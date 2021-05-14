import sys
import os
import pytest
import logging
# debug
import pprint

from sonic_cli_gen.yang_parser import YangParser

logger = logging.getLogger(__name__)

test_path = os.path.dirname(os.path.abspath(__file__))
config_db_path =  os.path.join(test_path, 'cli_autogen_input/config_db.json')
yang_models_path = '/usr/local/yang-models'


class TestYangParser:
    def test_one_table_container(self):
        yang_model_name = 'sonic-one-table-container'
        

        move_yang_model(yang_model_name)
        parser = YangParser(yang_model_name = yang_model_name,
                            config_db_path = config_db_path,
                            allow_tbl_without_yang = True,
                            debug = False)
        yang_dict = parser.parse_yang_model()
        pretty_log(yang_dict)

        pass

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
def pretty_log(dictionary):
    for line in pprint.pformat(dictionary).split('\n'):
        logging.warning(line)

