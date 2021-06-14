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

    ########## HASH-FIELD ##########

    def test_hash_field_add_no_ip_mask(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "1"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        logger.debug(result.stdout)

        assert result.exit_code == 0

    def test_hash_field_add_ip4_mask(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_dst_ipv4", "--hash-field", "INNER_DST_IPV4",
            "--ip-mask", "255.0.0.0",
            "--sequence-id", "3"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        logger.debug(result.stdout)

        assert result.exit_code == 0

    def test_hash_field_add_ip6_mask(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_dst_ipv6", "--hash-field", "INNER_DST_IPV6",
            "--ip-mask", "ffff::",
            "--sequence-id", "4"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        logger.debug(result.stdout)

        assert result.exit_code == 0

    ########## HASH-FIELD ##########

    #def test_config_pbh_table_add(self):
    #    db = Db()
    #    obj = { 'db': db.cfgdb }
    #    runner = CliRunner()
    #    result = runner.invoke(config.config.commands["pbh"].
    #        commands["table"].commands["add"],
    #        ["pbh_table", "--interface-list", "Ethernet0,Ethernet4",
    #        "--description", "NVGRE"], obj=obj)
    #    logger.debug(result.exit_code)
    #    logger.debug(result.output)
    #    #import pdb; pdb.set_trace()
    #    assert result.exit_code == 0
    #    #assert result.outup == correct_dict

    #def test_(self):
    #    db = Db()
    #    obj = { 'db': db.cfgdb }
    #    runner = CliRunner()

    #    result = runner.invoke(config.config.commands["pbh"].
    #        commands[""].commands["add"],
    #        ["", "--", "",
    #        "--", ""], obj=obj)

    #    logger.debug(result.stdout)
    #    logger.debug(result.exit_code)
    #    logger.debug(result.output)

    #    #assert result.exit_code == 0
    #    #assert result.outup == correct_dict

    #def test_config_pbh_hash_field(self):
    #    db = Db()
    #    obj = { 'db': db.cfgdb }
    #    runner = CliRunner()
    #    result = runner.invoke(config.config.commands["pbh"].
    #        commands["hash-field"].commands["add"],
    #        ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
    #        "--sequence-id", "1"], obj=obj)
    #    logger.debug(result.exit_code)
    #    logger.debug(result.output)
    #    #import pdb; pdb.set_trace()
    #    assert result.exit_code == 0
    #    # assert for dict


    @classmethod
    def teardown_class(cls):
        logger.info("TEARDOWN")
        os.environ['UTILITIES_UNIT_TESTING'] = "0"

