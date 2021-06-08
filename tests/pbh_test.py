#!/usr/bin/env python

import os
import logging
import show.main as show
import config.main as config

from utilities_common.db import Db
from click.testing import CliRunner


logger = logging.getLogger(__name__)
test_path = os.path.dirname(os.path.abspath(__file__))


class TestPBH:
    @classmethod
    def setup_class(cls):
        logger.info("SETUP")
        os.environ['UTILITIES_UNIT_TESTING'] = "1"


    def test_config_pbh_table_add(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()
        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["add"],
            ["pbh_table", "--interface-list", "Ethernet0,Ethernet4",
            "--description", "NVGRE"], obj=obj)
        logger.debug(result.exit_code)
        logger.debug(result.output)
        #import pdb; pdb.set_trace()
        assert result.exit_code == 0
        # assert for dict

    def test_config_pbh_hash_field(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()
        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "1"], obj=obj)
        logger.debug(result.exit_code)
        logger.debug(result.output)
        #import pdb; pdb.set_trace()
        assert result.exit_code == 0
        # assert for dict


    @classmethod
    def teardown_class(cls):
        logger.info("TEARDOWN")
        os.environ['UTILITIES_UNIT_TESTING'] = "0"

