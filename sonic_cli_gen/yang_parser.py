#!/usr/bin/env python

try:
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

    def parse_yang_model(self) -> dict:
        """ Parse proviced YANG model
            and save output to self.yang_2_dict obj 

            Returns:
                dictionary - parsed YANG model in dictionary format
        """

        self._init_yang_module_and_containers()
        self.yang_2_dict['tables'] = list()

        # determine how many (1 or couple) containers YANG model have after 'top level' container
        # 'table' container it is a container that goes after 'top level' container
        if isinstance(self.y_table_containers, list):
            for tbl_cont in self.y_table_containers:
                y2d_elem = on_table_container(tbl_cont)
                self.yang_2_dict['tables'].append(y2d_elem)
        else:
            y2d_elem = on_table_container(self.y_table_containers)
            self.yang_2_dict['tables'].append(y2d_elem)
    
        return self.yang_2_dict

def get_description(y_entity: OrderedDict) -> str:
    """ Parse 'description' entity from any YANG element

        Args:
            y_entity: reference to YANG 'container' OR 'list' OR 'leaf' ...
        Returns:
            str - text of the 'description'
    """

    if y_entity.get('description') is not None:
        return y_entity.get('description').get('text')
    else:
        return ''

def on_table_container(tbl_cont: OrderedDict) -> dict:
    """ Parse 'table' container,
        'table' container goes after 'top level' container

        Args:
            tbl_cont: reference to 'table' container
        Returns:
            dictionary - element for self.yang_2_dict['tables'] 
    """

    y2d_elem = {
        'name': tbl_cont.get('@name'),
        'description': get_description(tbl_cont),
        'dynamic-objects': list(),
        'static-objects': list()
    }

    # determine if 'container' have a 'list' entity
    tbl_cont_lists = tbl_cont.get('list')

    if tbl_cont_lists is None:
        is_list = False
        # 'object' container goes after 'table' container
        # 'object' container have 2 types - list (like sonic-flex_counter.yang) and NOT list (like sonic-device_metadata.yang)
        obj_cont = tbl_cont.get('container')
        if isinstance(obj_cont, list):
            for cont in obj_cont:
                static_obj_elem = on_container(cont, is_list)
                y2d_elem['static-objects'].append(static_obj_elem)
        else:
            static_obj_elem = on_container(obj_cont, is_list)
            y2d_elem['static-objects'].append(static_obj_elem)
    else:
        is_list = True
        # 'container' can have more than 1 'list'
        if isinstance(tbl_cont_lists, list):
            for _list in tbl_cont_lists:
                dynamic_obj_elem = on_container(_list, is_list)
                y2d_elem['dynamic-objects'].append(dynamic_obj_elem)
        else:
            dynamic_obj_elem = on_container(tbl_cont_lists, is_list)
            y2d_elem['dynamic-objects'].append(dynamic_obj_elem)

    return y2d_elem

def on_container(cont: OrderedDict, is_list: bool) -> dict:
    """ Parse a 'container' that have only 'leafs' or 'list' with 'leafs'

        Args:
            cont: reference to 'container'
        Returns:
            dictionary - element for y2d_elem['static-objects'] OR y2d_elem['dynamic-objects']
    """

    obj_elem = {
        'name': cont.get('@name'),
        'description': get_description(cont),
        'attrs': list()
    }

    if is_list:
        obj_elem['key'] = cont.get('key').get('@value')

    attrs_list = list()

    if cont.get('leaf') is not None:
        is_leaf_list = False
        ret_leafs = on_leafs(cont.get('leaf'), is_leaf_list)
        attrs_list.extend(ret_leafs)

    if cont.get('leaf-list') is not None:
        is_leaf_list = True
        ret_leaf_lists = on_leafs(cont.get('leaf-list'), is_leaf_list)
        attrs_list.extend(ret_leaf_lists)

    if cont.get('choice') is not None:
        y_choices = cont.get('choice')
        ret_choice_leafs = on_choices(y_choices)
        attrs_list.extend(ret_choice_leafs)

    obj_elem['attrs'] = attrs_list

    return obj_elem

def on_choices(y_choices) -> list:
    """ Parse a YANG 'choice' entities

        Args:
            cont: reference to 'choice'
        Returns:
            dictionary - element for obj_elem['attrs'], 'attrs' contain a parsed 'leafs'
    """

    ret_attrs = list()

    # the YANG model can have multiple 'choice' entities inside 'container' or 'list'
    if isinstance(y_choices, list):
        for choice in y_choices:
            attrs = on_choice_cases(choice.get('case'))
            ret_attrs.extend(attrs)
    else:
        ret_attrs = on_choice_cases(y_choices.get('case'))

    return ret_attrs

def on_choice_cases(y_cases: list) -> list:
    """ Parse a single YANG 'case' entity from 'choice' entity

        Args:
            cont: reference to 'case'
        Returns:
            dictionary - element for obj_elem['attrs'], 'attrs' contain a parsed 'leafs'
    """

    ret_attrs = list()

    if isinstance(y_cases, list):
        for case in y_cases:
            if case.get('leaf') is not None:
                is_leaf_list = False
                ret_leafs = on_leafs(case.get('leaf'), is_leaf_list)
                ret_attrs.extend(ret_leafs)

            if case.get('leaf-list') is not None:
                is_leaf_list = True
                ret_leaf_lists = on_leafs(case.get('leaf-list'), is_leaf_list)
                ret_attrs.extend(ret_leaf_lists)
    else:
        raise Exception('It has no sense to using a single "case" element inside "choice" element')
    
    return ret_attrs

def on_leafs(y_leafs, is_leaf_list: bool) -> list:
    """ Parse all the 'leaf' or 'leaf-list' elements

        Args:
            y_leafs: reference to all 'leaf' elements
        Returns:
            list - list of parsed 'leaf' elements 
    """

    ret_attrs = list()
    # The YANG 'container' entity may have only 1 'leaf' element OR a list of 'leaf' elements
    if isinstance(y_leafs, list): 
        for leaf in y_leafs:
            attr = on_leaf(leaf, is_leaf_list)
            ret_attrs.append(attr)
    else:
        attr = on_leaf(y_leafs, is_leaf_list)
        ret_attrs.append(attr)

    return ret_attrs

def on_leaf(leaf: OrderedDict, is_leaf_list: bool) -> dict:
    """ Parse a single 'leaf' element

        Args:
            leaf: reference to a 'leaf' entity
        Returns:
            dictionary - parsed 'leaf' element
    """

    mandatory = False
    if leaf.get('mandatory') is not None:
        mandatory = True

    attr = { 'name': leaf.get('@name'),
             'description': get_description(leaf),
             'is-leaf-list': is_leaf_list,
             'mandatory': mandatory }
    return attr