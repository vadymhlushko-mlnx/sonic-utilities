#!/usr/bin/env python

try:
    import pdb
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
        self.y_module = None
        # top level 'container' entity from .yang file
        self.y_top_level_container = None
        # 'container' entities from .yang file that represent Config DB table
        self.y_table_containers = None
        # dictionary that represent Config DB schema
        self.yang_2_dict = dict()

        try:
            self.conf_mgmt = ConfigMgmt()
        except Exception as e:
            raise Exception("Failed to load the {} class".format(str(e)))

    def parse_yang_model(self):
        self._init_yang_module_and_containers()

        # determine how many (1 or couple) containers yang model have after 'top level container'
        if isinstance(self.y_table_containers, list):
            print('LIST')
            for tbl_cont in self.y_table_containers:
                self._fill_yang_2_dict(tbl_cont)
        else:
            print('NOT LIST')
            self._fill_yang_2_dict(self.y_table_containers)


    def _fill_yang_2_dict(self, tbl_cont):
        self.yang_2_dict['tables'] = list()
        # element for self.yang_2_dict list
        y2d_elem = dict()
        
        y2d_elem['name'] = tbl_cont.get('@name')
        y2d_elem['description'] = ''
        if tbl_cont.get('description') is not None:
            y2d_elem['description'] = tbl_cont.get('description').get('text')
        y2d_elem['dynamic-objects'] = list()
        y2d_elem['static-objects'] = list()

        # determine if 'container' is a 'list' or 'static'
        # 'static' means that yang model 'container' entity does NOT have a 'list' entity
        if tbl_cont.get('list') is None:
            # TODO write comment about objects containers inside table containers
            obj_cont = tbl_cont.get('container')
            if isinstance(obj_cont, list):
                # flex counter
                print ("FLEX")
                for cont in obj_cont:
                    self._on_static_container(cont, y2d_elem)
            else:
                print ("METADATA")
                # device metadata
                self._on_static_container(obj_cont, y2d_elem)
        else:
            self._on_list_container(tbl_cont, y2d_elem)

        self.yang_2_dict['tables'].append(y2d_elem)
        pdb.set_trace()

    def _on_static_container(self, cont, y2d_elem):
        # element for y2d_elem['static-objects']
        static_obj_elem = dict()
        static_obj_elem['name'] = cont.get('@name')
        static_obj_elem['description'] = ''
        if cont.get('description') is not None:
            static_obj_elem['description'] = cont.get('description').get('text')

        self._parse_yang_leafs(cont.get('leaf'), static_obj_elem, y2d_elem)

    def _parse_yang_leafs(self, y_leafs, static_obj_elem, y2d_elem):
        static_obj_elem['attrs'] = list()
        # The YANG 'container entity may have only 1 'leaf' element or list of 'leaf' elements
        if isinstance(y_leafs, list): 
            for leaf in y_leafs:
                attr = dict()
                attr['name'] = leaf.get('@name')
                attr['is-leaf-list'] = leaf.get('__isleafList')
                static_obj_elem['attrs'].append(attr)

            y2d_elem['static-objects'].append(static_obj_elem)
        else:
            attr = dict()
            attr['name'] = y_leafs.get('@name')
            attr['is-leaf-list'] = y_leafs.get('__isleafList')
            static_obj_elem['attrs'].append(attr)
            y2d_elem['static-objects'].append(static_obj_elem)

    def _on_list_container(self, cont, y2d_elem):
        pass

    def _init_yang_module_and_containers(self):
        self._find_index_of_yang_model()

        self.y_module = self.conf_mgmt.sy.yJson[self.idx_yJson]['module']
        if self.y_module.get('container') is not None:
            self.y_top_level_container = self.y_module['container']
            self.y_table_containers = self.y_top_level_container['container']
        else:
            raise KeyError('YANG model {} does NOT have "container" element'.format(self.yang_model_name))

    # find index of yang_model inside yJson object
    def _find_index_of_yang_model(self):
        for i in range(len(self.conf_mgmt.sy.yJson)):
            if (self.conf_mgmt.sy.yJson[i]['module']['@name'] == self.yang_model_name):
                self.idx_yJson = i


            
        
       