import sys
import os
import pytest
import logging
# debug
import pprint

from sonic_cli_gen.yang_parser import YangParser
from .cli_autogen_input import assert_dictionaries


logger = logging.getLogger(__name__)

test_path = os.path.dirname(os.path.abspath(__file__))
yang_models_path = '/usr/local/yang-models'


class TestYangParser:

    #create function like 'start' which copy all YANG to location
    #create function teardown

    def test_1_table_container(self):
        yang_model_name = 'sonic-1-table-container'
        template(yang_model_name, assert_dictionaries.one_table_container)
       
    def test_2_table_containers(self):
        yang_model_name = 'sonic-2-table-containers'
        template(yang_model_name, assert_dictionaries.two_table_containers)

    def test_1_object_container(self):
        yang_model_name = 'sonic-1-object-container'
        template(yang_model_name, assert_dictionaries.one_object_container)

    def test_2_object_containers(self):
        yang_model_name = 'sonic-2-object-containers'
        template(yang_model_name, assert_dictionaries.two_object_containers)

    def test_1_list(self):
        yang_model_name = 'sonic-1-list'
        template(yang_model_name, assert_dictionaries.one_list)

    def test_2_lists(self):
        yang_model_name = 'sonic-2-lists'
        template(yang_model_name, assert_dictionaries.two_lists)

    def test_static_object_complex_1(self):
        """ Test object container with: 1 leaf, 1 leaf-list, 1 choice.
        """
        yang_model_name = 'sonic-static-object-complex-1'
        template(yang_model_name, assert_dictionaries.static_object_complex_1)

    def test_static_object_complex_2(self):
        """ Test object container with: 2 leafs, 2 leaf-lists, 2 choices.
        """
        yang_model_name = 'sonic-static-object-complex-2'
        template(yang_model_name, assert_dictionaries.static_object_complex_2)

    def test_dynamic_object_complex_1(self):
        """ Test object container with: 1 key, 1 leaf, 1 leaf-list, 1 choice.
        """
        yang_model_name = 'sonic-dynamic-object-complex-1'
        template(yang_model_name, assert_dictionaries.dynamic_object_complex_1)

    def test_dynamic_object_complex_2(self):
        """ Test object container with: 2 keys, 2 leafs, 2 leaf-list, 2 choice.
        """
        yang_model_name = 'sonic-dynamic-object-complex-2'
        template(yang_model_name, assert_dictionaries.dynamic_object_complex_2)

    def test_choice_complex(self):
        """ Test object container with choice that have complex strucutre:
            leafs, leaf-lists, multiple 'uses' from different files
        """
        yang_model_name = 'sonic-choice-complex'
        grouping_yang_1 = 'sonic-grouping-1'
        grouping_yang_2 = 'sonic-grouping-2'
        move_yang_model(grouping_yang_1)
        move_yang_model(grouping_yang_2)
        template(yang_model_name, assert_dictionaries.choice_complex)
        remove_yang_model(grouping_yang_1)
        remove_yang_model(grouping_yang_2)

    def test_choice_complex(self):
        """ Test object container with muplitple 'uses' that using 'grouping'
            from different files. The used 'grouping' have a complex strucutre:
            leafs, leaf-lists, choices
        """
        yang_model_name = 'sonic-grouping-complex'
        grouping_yang_1 = 'sonic-grouping-1'
        grouping_yang_2 = 'sonic-grouping-2'
        move_yang_model(grouping_yang_1)
        move_yang_model(grouping_yang_2)
        template(yang_model_name, assert_dictionaries.grouping_complex)
        remove_yang_model(grouping_yang_1)
        remove_yang_model(grouping_yang_2)

def template(yang_model_name, correct_dict):
    config_db_path =  os.path.join(test_path, 'cli_autogen_input/config_db.json')
    move_yang_model(yang_model_name)
    parser = YangParser(yang_model_name = yang_model_name,
                        config_db_path = config_db_path,
                        allow_tbl_without_yang = True,
                        debug = False)
    yang_dict = parser.parse_yang_model()

    pretty_log_debug(yang_dict)

    assert yang_dict == correct_dict

    remove_yang_model(yang_model_name)

def move_yang_model(yang_model_name):
    """ Move provided YANG model to known location for YangParser class

        Args:
            yang_model_name: name of provided YANG model
    """
    src_path = os.path.join(test_path, 'cli_autogen_input', yang_model_name + '.yang')
    cmd = 'sudo cp {} {}'.format(src_path, yang_models_path)
    os.system(cmd)

def remove_yang_model(yang_model_name):
    """ Remove YANG model from well known system location

        Args:
            yang_model_name: name of provided YANG model
    """
    yang_model_path = os.path.join(yang_models_path, yang_model_name + '.yang')
    cmd = 'sudo rm {}'.format(yang_model_path)
    os.system(cmd)

# DEBUG function
def pretty_log_debug(dictionary):
    for line in pprint.pformat(dictionary).split('\n'):
        logging.debug(line)

