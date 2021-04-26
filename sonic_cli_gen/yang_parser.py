#!/usr/bin/env python

try:
    import os
    import sys
    import pprint
    from config.config_mgmt import ConfigMgmt
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

# Config DB schema view
STATIC_TABLE = 'static'
LIST_TABLE = 'list'

class YangParser:
    """ YANG model parser """
    def __init__(self,
                 yang_model_name):
        self.yang_model_name = yang_model_name
        self.conf_mgmt = None

        try:
            self.conf_mgmt = ConfigMgmt()
        except Exception as e:
            raise Exception("Failed to load the {} class".format(str(e)))

    def fail(self, e):
        print(e)
        raise e

    def yang_to_dict(self):
        yang_model_type = self._determine_yang_model_type()

    def _determine_yang_model_type(self):
         y_index = self._find_index_of_yang_model()
         print("INDEX {}".format(y_index))

    def _find_index_of_yang_model(self):
        for i in range(len(self.conf_mgmt.sy.yJson)):
            if (self.conf_mgmt.sy.yJson[i]['module']['@name'] == self.yang_model_name):
                return i


            
        
       