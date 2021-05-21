#!/usr/bin/env python

import os
import pkgutil
import jinja2

from sonic_cli_gen.yang_parser import YangParser

class CliGenerator:
    """ SONiC CLI generator. This class provides public API
    for sonic-cli-gen python library. It can generate config,
    show CLI plugins
    """

    def __init__(self):
        """ Initialize PackageManager. """

        self.loader = jinja2.FileSystemLoader(['/usr/share/sonic/templates/sonic-cli-gen/'])
        self.env = jinja2.Environment(loader=self.loader)


    def generate_cli_plugin(self, cli_group, plugin_name):
        """ Generate click CLI plugin. """

        parser = YangParser(yang_model_name=plugin_name,
                            config_db_path='configDB',
                            allow_tbl_without_yang=True,
                            debug=False)
        # yang_dict will be used as an input for templates located in - /usr/share/sonic/templates/sonic-cli-gen/
        yang_dict = parser.parse_yang_model()
        plugin_path = get_cli_plugin_path(cli_group, plugin_name + '_yang.py')
        template = self.env.get_template(cli_group + '.py.j2')
        with open(plugin_path, 'w') as plugin_py:
            plugin_py.write(template.render(yang_dict))
            print('\nAuto-generation successful!\nLocation: {}'.format(plugin_path))

    
    def remove_cli_plugin(self, cli_group, plugin_name):
        plugin_path = get_cli_plugin_path(cli_group, plugin_name + '_yang.py')
        if os.path.exists(plugin_path):
            os.remove(plugin_path)
            print('{} was removed.'.format(plugin_path))
        else:
            print('Path {} doest NOT exist!'.format(plugin_path))


def get_cli_plugin_path(command, plugin_name):
    pkg_loader = pkgutil.get_loader(f'{command}.plugins.auto')
    if pkg_loader is None:
        raise Exception(f'Failed to get plugins path for {command} CLI')
    plugins_pkg_path = os.path.dirname(pkg_loader.path)

    return os.path.join(plugins_pkg_path, plugin_name)

