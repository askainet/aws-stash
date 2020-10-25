# -*- coding: utf-8 -*-

# The maximum length for the fully qualified parameter name is 1011 characters.
# A hierarchy can have a maximum of 15 levels.
# The maximum length for the string value is 4096.

from aws_stash import __project_name__, __version__

import sys

from aws_stash.ParamStore import ParamStore
from aws_stash.Output import Output


def main():
    def valid_path(value):
        if value is None:
            return value
        import re
        pattern = '^/(([A-Za-z0-9-_.]+)/?)*$'
        if not re.match(pattern, value):
            raise argparse.ArgumentTypeError(
                "{0} is an invalid path, must match pattern '{1}'' ".format(value, pattern))
        return value

    import argparse
    import itertools

    parser = argparse.ArgumentParser()

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__), help='Show version')
    parser.add_argument('path', type=valid_path,
                        help='Path to the parameter key or folder containing parameter keys')
    parser.add_argument('-p', '--params', nargs='+',
                        action='append', default=[], help='Parameter keys')
    parser.add_argument('-w', '--write', nargs='?', const='',
                        help='Write parameter value, leave it empty to input it from STDIN')
    parser.add_argument('-m', '--multi-line', action='store_true',
                        help='Accept multi-line value from STDIN, end input with CTRL+D')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force overwrite existing value')
    parser.add_argument('-d', '--description', default=None,
                        help='Add a description to the parameter')
    parser.add_argument('-k', '--kms', default='aws/ssm',
                        help='KMS key alias to encrypt the value')
    parser.add_argument('-c', '--copy', action='store_true',
                        help='Copy value to the clipboard instead of showing it')
    parser.add_argument('-o', '--output', choices=['text', 'json', 'export'],
                        default='text', help='Output format')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List all paramaters under same level path')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Process all paramaters recursively starting from path')
    parser.add_argument('--delete', action='store_true',
                        help='Delete a single parameter or all parameters recursively starting from path if using --recursive')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Output only the values of the parameters')
    parser.add_argument('--full', action='store_true',
                        help='Output fully qualified parameter path')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Output parameters details')
    parser.add_argument('--find-in-parents', action='store_true',
                        help='Find a key in parent folders')

    args = parser.parse_args()

    args.params = list(set(itertools.chain.from_iterable(args.params)))

    param_store = ParamStore()
    output = Output()

    if args.write is not None:
        version = param_store.write_parameter(
            path=args.path,
            value=args.write,
            description=args.description,
            force=args.force,
            multi_line=args.multi_line,
            kms=args.kms
        )
        if version is None:
            sys.exit(1)
        if not args.quiet:
            print('Version: {}'.format(version))

    elif args.delete:
        version = param_store.delete_parameters(
            path=args.path,
            recursive=args.recursive
        )

    else:
        if args.list:
            parameters = param_store.list_parameters(
                path=args.path,
                recursive=args.recursive,
                params=args.params,
                verbose=args.verbose
            )
        else:
            parameters = param_store.get_parameters(
                path=args.path,
                params=args.params,
                find_in_parents=args.find_in_parents,
                verbose=args.verbose
            )

        if len(parameters):
            output.output(args, parameters)
        if not len(parameters) or (
                args.params and len(parameters) != len(args.params)):
            sys.exit(1)


if __name__ == '__main__':
    main()
