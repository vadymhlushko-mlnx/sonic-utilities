#!/usr/bin/env python

try:
    from sonic_cli_gen.yang_parser import YangParser
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

class CliGenerator:
    """ SONiC CLI generator. This class provides public API
    for sonic-cli-gen python library. It can generate config,
    show, sonic-clear CLI plugins
    """

    def __init__(self,
                 yang_model):
        """ Initialize PackageManager. """

        self.yang_model_name = yang_model

    def generate_config_plugin(self):
        """ Generate CLI plugin for 'config' CLI group. """
        parser = YangParser(self.yang_model_name)
        yang_dict = parser.parse_yang_model()
        pass

    def generate_show_plugin(self):
        """ Generate CLI plugin for 'show' CLI group. """
        parser = YangParser(self.yang_model_name)
        yang_dict = parser.parse_yang_model()
        pass

    # to be implemented in the next Phases
    def generate_sonic_clear_plugin(self):
        """ Generate CLI plugin for 'sonic-clear' CLI group. """
        parser = YangParser(self.yang_model_name)
        yang_dict = parser.parse_yang_model()
        pass
