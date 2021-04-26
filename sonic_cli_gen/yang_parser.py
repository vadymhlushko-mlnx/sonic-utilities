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
        #index of yang model inside conf_mgmt.sy.yJson object
        self.idx_yJson = None
        self.y_module = None
        self.y_top_level_container = None
        self.y_tables = None

        try:
            self.conf_mgmt = ConfigMgmt()
        except Exception as e:
            raise Exception("Failed to load the {} class".format(str(e)))

    def fail(self, e):
        print(e)
        raise e

    def parse_yang_model(self):
        self._init_yang_module_and_containers()

    def _determine_tables_type(self):
        #for table in y_top_level_container['container']:
        pass

    def _init_yang_module_and_containers(self):
        self._find_index_of_yang_model()

        self.y_module = self.conf_mgmt.sy.yJson[self.idx_yJson]['module']
        if self.y_module.get('container') is not None:
            self.y_top_level_container = self.y_module['container']
            self.y_tables = self.y_top_level_container['container']
            import pdb; pdb.set_trace()
        else:
            raise KeyError('YANG model {} does NOT have "container" element'.format(self.yang_model_name))

    # find index of yang_model inside yJson object
    def _find_index_of_yang_model(self):
        for i in range(len(self.conf_mgmt.sy.yJson)):
            if (self.conf_mgmt.sy.yJson[i]['module']['@name'] == self.yang_model_name):
                self.idx_yJson = i


            
        
       