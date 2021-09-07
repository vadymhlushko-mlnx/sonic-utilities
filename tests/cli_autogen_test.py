import os
import logging
import pprint

import sonic_cli_gen.main as cli_gen

from sonic_cli_gen.generator import CliGenerator
from click.testing import CliRunner
from utilities_common.db import Db

logger = logging.getLogger(__name__)

test_path = os.path.dirname(os.path.abspath(__file__))
yang_models_path = '/usr/local/yang-models'


class TestCliAutogen:
    @classmethod
    def setup_class(cls):
        logger.info("SETUP")
        os.environ['UTILITIES_UNIT_TESTING'] = "2"

    @classmethod
    def teardown_class(cls):
        logger.info("TEARDOWN")
        os.environ['UTILITIES_UNIT_TESTING'] = "0"

    def test_one(self):
        runner = CliRunner()
        db = Db()
        obj = {'config_db': db.cfgdb}

        gen = CliGenerator(logger) 
        res = gen.generate_cli_plugin('config', 'sonic-device_metadata')

