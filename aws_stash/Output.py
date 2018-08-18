# -*- coding: utf-8 -*-

import pyperclip


class Output:
    def text(self, options, parameters):
        for parameter in parameters:
            name = parameter['Name'] if options.full or options.list else parameter['Name'].split('/')[-1]
            if options.list:
                print(name)
            elif options.quiet:
                print(parameter['Value'])
            elif options.verbose:
                print('{0}="{1}" version={2} description={3}'.format(name, parameter['Value'], parameter['Version'], parameter.get('Description')))
            else:
                print('{0}="{1}"'.format(name, parameter['Value']))

    def export(self, options, parameters):
        for parameter in parameters:
            name = parameter['Name'] if options.full or options.list else parameter['Name'].split('/')[-1]
            print('export {0}="{1}"'.format(name, parameter['Value']))

    def json(self, options, parameters):
        import json
        output = dict()
        for parameter in parameters:
            name = parameter['Name'] if options.full or options.list else parameter['Name'].split('/')[-1]
            if not options.list:
                if options.verbose:
                    output[name] = {
                        'Value': parameter['Value'],
                        'Version': parameter['Version'],
                        'Description': parameter.get('Description')
                    }
                else:
                    output[name] = parameter['Value']
        if options.list:
            output = list(output.keys())
        elif options.quiet:
            values = list(output.values())
            output = values if len(values) > 1 else values[0]

        print(json.dumps(output, sort_keys=True, indent=2))

    def clipboard(self, options, parameters):
        if len(parameters) == 1:
            pyperclip.copy(parameters[0]['Value'])
            return True
        else:
            return False

    def output(self, options, parameters):
        if options.copy:
            if self.clipboard(options, parameters):
                return
        if options.output == 'text':
            self.text(options, parameters)
        if options.output == 'export':
            self.export(options, parameters)
        elif options.output == 'json':
            self.json(options, parameters)
