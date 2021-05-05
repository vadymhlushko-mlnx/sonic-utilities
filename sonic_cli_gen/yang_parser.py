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
    """ YANG model parser

        Attributes:
        yang_model_name: Name of the YANG model file
        conf_mgmt: Instance of Config Mgmt class to help parse YANG models
        idx_yJson: Index of YANG model file (1 attr) inside conf_mgmt.sy.yJson object
        y_module: Reference to 'module' entity from YANG model file
        y_top_level_container: Reference to top level 'container' entity from YANG model file
        y_table_containers: Reference to 'container' entities from YANG model file
                            that represent Config DB tables
        yang_2_dict: dictionary created from YANG model file that represent Config DB schema
    """
    def __init__(self,
                 yang_model_name):
        self.yang_model_name = yang_model_name
        self.conf_mgmt = None
        self.idx_yJson = None
        self.y_module = None
        self.y_top_level_container = None
        self.y_table_containers = None
        self.yang_2_dict = dict()

        try:
            self.conf_mgmt = ConfigMgmt()
        except Exception as e:
            raise Exception("Failed to load the {} class".format(str(e)))
    
    def _init_yang_module_and_containers(self):
        """ Initialize inner class variables:
            self.y_module
            self.y_top_level_container
            self.y_table_containers

            Raises:
                KeyError: if invalid YANG model provided
                KeyError: if YANG models is NOT exist
        """

        self._find_index_of_yang_model()

        if self.idx_yJson is not None:
            self.y_module = self.conf_mgmt.sy.yJson[self.idx_yJson]['module']
            if self.y_module.get('container') is not None:
                self.y_top_level_container = self.y_module['container']
                self.y_table_containers = self.y_top_level_container['container']
            else:
                raise KeyError('YANG model {} does NOT have "container" element'.format(self.yang_model_name))
        else:
            raise KeyError('YANG model {} is NOT exist'.format(self.yang_model_name))

    def _find_index_of_yang_model(self):
        """ Find index of provided YANG model inside yJson object
            and save it to self.idx_yJson variable
        """

        for i in range(len(self.conf_mgmt.sy.yJson)):
            if (self.conf_mgmt.sy.yJson[i]['module']['@name'] == self.yang_model_name):
                self.idx_yJson = i

    def parse_yang_model(self):
        """ Parse proviced YANG model
            and save output to self.yang_2_dict obj 
        """

        self._init_yang_module_and_containers()
        self.yang_2_dict['tables'] = list()

        # determine how many (1 or couple) containers yang model have after 'top level container'
        if isinstance(self.y_table_containers, list):
            for tbl_cont in self.y_table_containers:
                y2d_elem = on_table_container(tbl_cont)
                self.yang_2_dict['tables'].append(y2d_elem)
        else:
            y2d_elem = on_table_container(self.y_table_containers)
            self.yang_2_dict['tables'].append(y2d_elem)

        pdb.set_trace()

def on_table_container(tbl_cont: OrderedDict) -> dict:
    """ Parse 'table' container,
        'table' container goes after 'top level' container

        Args:
            tbl_cont: reference to 'table' container
        Returns:
            dictionary - element for self.yang_2_dict['tables'] 
    """

    if tbl_cont.get('description') is not None:
        description = tbl_cont.get('description').get('text')
    else:
        description = ''

    y2d_elem = {
        'name': tbl_cont.get('@name'),
        'description': description,
        'dynamic-objects': list(),
        'static-objects': list()
    }

    # determine if 'container' is a 'list' or 'static'
    # 'static' means that yang model 'container' entity does NOT have a 'list' entity
    if tbl_cont.get('list') is None:
        # 'object' container goes after 'table' container
        # 'object' container have 2 types - list (like sonic-flex_counter.yang) and NOT list (like sonic-device_metadata.yang)
        obj_cont = tbl_cont.get('container')
        if isinstance(obj_cont, list):
            for cont in obj_cont:
                static_obj_elem = on_static_container(cont)
                y2d_elem['static-objects'].append(static_obj_elem)
        else:
            static_obj_elem = on_static_container(obj_cont)
            y2d_elem['static-objects'].append(static_obj_elem)
    else:
        on_list_container(tbl_cont)

    return y2d_elem

def on_static_container(cont: OrderedDict) -> dict:
    """ Parse container that does NOT have a 'list' entity ('static')

        Args:
            cont: reference to 'static' container
        Returns:
            dictionary - element for y2d_elem['static-objects']
    """

    if cont.get('description') is not None:
        description = cont.get('description').get('text')
    else:
        description = ''

    static_obj_elem = {
        'name': cont.get('@name'),
        'description': description,
        'attrs': list()
    }
    static_obj_elem['attrs'] = parse_yang_leafs(cont.get('leaf'))

    return static_obj_elem

def parse_yang_leafs(y_leafs) -> list:
    """ Parse all the 'leafs'

        Args:
            y_leafs: reference to all 'leaf' elements
        Returns:
            list - list of parsed 'leafs'
    """
    ret_attrs_list = list()
    # The YANG 'container' entity may have only 1 'leaf' element OR a list of 'leaf' elements
    if isinstance(y_leafs, list): 
        for leaf in y_leafs:
            attr = on_leaf(leaf)
            ret_attrs_list.append(attr)
    else:
        attr = on_leaf(y_leafs)
        ret_attrs_list.append(attr)

    return ret_attrs_list

def on_leaf(leaf: OrderedDict) -> dict:
    """ Parse a single 'leaf' element

        Args:
            leaf: reference to a 'leaf' entity
        Returns:
            dictionary - parsed 'leaf' element
    """
    mandatory = False
    if leaf.get('mandatory') is not None:
        mandatory = leaf.get('mandatory').get('@value')

    attr = { 'name': leaf.get('@name'),
             'is-leaf-list': leaf.get('__isleafList'),
             'mandatory': mandatory }
    return attr

def on_list_container(cont):
    pass