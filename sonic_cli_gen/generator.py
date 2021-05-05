#!/usr/bin/env python

try:
    from sonic_cli_gen.yang_parser import YangParser
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

class CliGenerator:
    """ SONiC CLI generator. This class provides public API
    for sonic-cli-gen python library. It can generate config,
    show, sonic-clear commands
    """

    def __init__(self,
                 yang_model):
        """ Initialize PackageManager. """

        self.yang_model_name = yang_model

    def generate_config_plugin(self):
        parser = YangParser(self.yang_model_name)
        parser.parse_yang_model()
        pass

    #TODO
    def generate_show_plugin(self):
        print ("show")
        pass

    # to be implemented in the next Phases
    def generate_sonic_clear_plugin(self):
        print ("sonic-clear")
        pass
