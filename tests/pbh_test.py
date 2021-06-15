#!/usr/bin/env python

import os
import logging
import show.main as show
import config.main as config

from utilities_common.db import Db
from click.testing import CliRunner


logger = logging.getLogger(__name__)
test_path = os.path.dirname(os.path.abspath(__file__))

SUCCESS = 0
ERROR = 1


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

        assert result.exit_code == SUCCESS

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

        assert result.exit_code == SUCCESS

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

        assert result.exit_code == SUCCESS

    # negative add: --hash-field & --ip-mask mismatch
    def test_hash_field_add_hash_field_with_ip(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_protocol", "--hash-field", "INNER_IP_PROTOCOL",
            "--ip-mask", "255.0.0.0",
            "--sequence-id", "1"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR

    # negative add: --hash-field v6 & --ip-mask v4 mismatch
    def test_hash_field_add_ipv4_mismatch(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv6", "--hash-field", "INNER_SRC_IPV6",
            "--ip-mask", "255.0.0.0",
            "--sequence-id", "4"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR

    # negative add: --hash-field v4 & --ip-mask v6 mismatch
    def test_hash_field_add_ipv6_mismatch(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv4", "--hash-field", "INNER_SRC_IPV4",
            "--ip-mask", "ffff::",
            "--sequence-id", "2"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR

    # negative add: invalid --ip-mask
    def test_hash_field_add_invalid_ip(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv4", "--hash-field", "INNER_SRC_IPV4",
            "--ip-mask", "WRONG",
            "--sequence-id", "2"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR

    # negative add: None --ip-mask
    def test_hash_field_add_none_ipv4(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv4", "--hash-field", "INNER_SRC_IPV4",
            "--sequence-id", "2"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR

    # negative add: None --ip-mask
    def test_hash_field_add_none_ipv6(self):
        db = Db()
        obj = { 'db': db.cfgdb }
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv6", "--hash-field", "INNER_SRC_IPV6",
            "--sequence-id", "2"], obj=obj)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR

    ########## HASH-FIELD ##########

    @classmethod
    def teardown_class(cls):
        logger.info("TEARDOWN")
        os.environ['UTILITIES_UNIT_TESTING'] = "0"

