#!/usr/bin/env python

try:
    import os
    import sys
    import pprint
    from collections import OrderedDict
    from config.config_mgmt import ConfigMgmt
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

class YangParser:
    """ YANG model parser """
    def __init__(self,
                 yang_model_name):
        self.yang_model_name = yang_model_name
        self.conf_mgmt = None
        # index of yang model inside conf_mgmt.sy.yJson object
        self.idx_yJson = None
        # 'module' entity from .yang file
        self.y_module = OrderedDict()
        # top level 'container' entity from .yang file
        self.y_top_level_container = OrderedDict()
        # 'container' entities from .yang file
        self.y_tables = list()
        # dictionary that represent Config DB schema
        self.yang_2_dict = OrderedDict()

        try:
            self.conf_mgmt = ConfigMgmt()
        except Exception as e:
            raise Exception("Failed to load the {} class".format(str(e)))

    def fail(self, e):
        print(e)
        raise e

    def parse_yang_model(self):
        self._init_yang_module_and_containers()

        self._determine_tables_type()

    def _determine_tables_type(self):
        for table in self.y_tables:
            if table.get('list') is None:
                self.yang_2_dict[table.get('@name')] = {'type': 'static'}
            else:
                self.yang_2_dict[table.get('@name')] = {'type': 'list'}

    def _init_yang_module_and_containers(self):
        self._find_index_of_yang_model()

        self.y_module = self.conf_mgmt.sy.yJson[self.idx_yJson]['module']
        if self.y_module.get('container') is not None:
            self.y_top_level_container = self.y_module['container']
            self.y_tables = self.y_top_level_container['container']
        else:
            raise KeyError('YANG model {} does NOT have "container" element'.format(self.yang_model_name))

    # find index of yang_model inside yJson object
    def _find_index_of_yang_model(self):
        for i in range(len(self.conf_mgmt.sy.yJson)):
            if (self.conf_mgmt.sy.yJson[i]['module']['@name'] == self.yang_model_name):
                self.idx_yJson = i


            
        
       