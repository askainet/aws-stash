# -*- coding: utf-8 -*-

# The maximum length for the fully qualified parameter name is 1011 characters.
# A hierarchy can have a maximum of 15 levels.
# The maximum length for the string value is 4096.

import sys
import boto3
from botocore.exceptions import ClientError


class ParamStore:
    def __init__(self):
        self.ssm_client = boto3.client('ssm')

    def get_parameter(self, path, verbose=False):
        try:
            if verbose:
                paginator = self.ssm_client.get_paginator(
                    'get_parameter_history')
                page_iterator = paginator.paginate(
                    Name=path,
                    WithDecryption=True
                )
                parameters = list()
                for page in page_iterator:
                    parameters = parameters + page['Parameters']

                if len(parameters):
                    return sorted(parameters, key=lambda k: k['Version'], reverse=True)[0]
                else:
                    return None

            else:
                response = self.ssm_client.get_parameter(
                    Name=path,
                    WithDecryption=True
                )
                return response.get('Parameter')

        except ClientError as e:
            if e.response['Error']['Code'] != 'ParameterNotFound':
                raise e

    def list_parameters(self, path, recursive=False, params=[], verbose=False):

        def add_paths(paths, levels, start_depth, recursive):
            if recursive:
                max_depth = len(levels)
            else:
                max_depth = min(len(levels), start_depth + 1)
            for i in range(start_depth, max_depth):
                path = '/'.join(levels[:i]) + '/'
                if path not in paths:
                    paths.append(path)

        start_depth = len(path.rstrip('/').split('/')) + 1
        parameters = list()
        paths = list()

        paginator = self.ssm_client.get_paginator('get_parameters_by_path')
        page_iterator = paginator.paginate(
            Path=path,
            WithDecryption=True,
            Recursive=True
        )

        for page in page_iterator:
            for parameter in page['Parameters']:
                levels = parameter['Name'].split('/')
                add_paths(paths, levels, start_depth, recursive)
                if not recursive:
                    # Skip parameters in sub-directories when recursive is not enabled
                    if len(levels) > start_depth:
                        continue

                if len(params):
                    print(levels)
                    print(params)
                    if levels[-1] not in params:
                        continue

                parameters.append({'Name': parameter['Name']})

        for path in paths:
            parameters.append({'Name': path})

        parameters = sorted(parameters, key=lambda k: k['Name'])

        if not len(parameters) and not len(params):
            parameter = self.get_parameter(path, verbose)
            if parameter:
                parameters.append(parameter)

        return parameters

    def __match_param(self, path, params, full_name):
        for p in params:
            if full_name == path+'/'+p:
                return p
        return False

    def get_parameters(self, path, params=[], find_in_parents=False, verbose=False):
        parameters = list()
        found = list()

        paginator = self.ssm_client.get_paginator('get_parameters_by_path')
        page_iterator = paginator.paginate(
            Path=path,
            WithDecryption=True
        )

        for page in page_iterator:
            for parameter in page['Parameters']:
                if len(params):
                    match = self.__match_param(path, params, parameter["Name"])
                    if not match:
                        continue
                    found.append(match)
                if verbose:
                    parameter = self.get_parameter(parameter['Name'], verbose)
                parameters.append(parameter)

        # try to get path as a parameter when no parameters requested
        # and none were found using get_parameters_by_path
        if not len(parameters) and not len(params):
            parameter = self.get_parameter(path, verbose)
            if parameter:
                parameters.append(parameter)

        # try to any missing parameters in parent folders when requested
        if find_in_parents and path != '/' and (
                len(params) == len(parameters) == 0
                or len(parameters) < len(params)):
            if len(params):
                params = list(set(params) - set(found))
            path = '/' + '/'.join(path.split('/')[1:-1])
            parameters += self.get_parameters(
                path=path, params=params,
                find_in_parents=find_in_parents, verbose=verbose)

        return parameters

    def write_parameter(self, path, value='', description=None, force=False, multi_line=False, kms='aws/kms'):
        if value == '':
            for line in sys.stdin:
                value = value + line
                if not multi_line:
                    break
            value = value[:-1]

        if description is None:
            parameter = self.get_parameter(path, verbose=True)
            if parameter:
                description = parameter.get('Description', '')
            else:
                description = ''

        try:
            response = self.ssm_client.put_parameter(
                Name=path,
                Value=value,
                Description=description,
                Type='SecureString',
                KeyId='alias/{}'.format(kms),
                Overwrite=force
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterAlreadyExists':
                print(
                    'Parameter {0} already exists, use --force if you want to overwrite its value'.format(path))
                return None
            else:
                raise e
        else:
            return response['Version']

    def delete_parameters(self, path, recursive=False):
        if recursive:
            list_params = self.list_parameters(
                path=path, recursive=recursive)
            parameters = [p['Name'] for p in list_params]
        else:
            parameters = [path]

        if len(parameters):
            response = self.ssm_client.delete_parameters(
                Names=parameters
            )
            print('Deleted parameters: {0}'.format(
                response['DeletedParameters']))
            print('Invalid parameters: {0}'.format(
                response['InvalidParameters']))
