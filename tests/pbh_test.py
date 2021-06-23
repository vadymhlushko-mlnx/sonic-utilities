#!/usr/bin/env python

import os
import logging
import show.main as show
import config.main as config

from .pbh_input import assert_show_output
from utilities_common.db import Db
from click.testing import CliRunner
from .mock_tables import dbconnector

logger = logging.getLogger(__name__)
test_path = os.path.dirname(os.path.abspath(__file__))
mock_db_path = os.path.join(test_path, "pbh_input")

SUCCESS = 0
ERROR = 1
ERROR2 = 2


class TestPBH:
    @classmethod
    def setup_class(cls):
        logger.info("SETUP")
        os.environ['UTILITIES_UNIT_TESTING'] = "1"

    @classmethod
    def teardown_class(cls):
        logger.info("TEARDOWN")
        os.environ['UTILITIES_UNIT_TESTING'] = "0"


    ########## CONFIG PBH HASH-FIELD ##########


    def test_config_pbh_hash_field_add_delete_no_ip_mask(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["delete"],
            ["inner_ip_proto"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS


    def test_config_pbh_hash_field_add_ip4_mask(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_dst_ipv4", "--hash-field", "INNER_DST_IPV4",
            "--ip-mask", "255.0.0.0",
            "--sequence-id", "3"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS


    def test_config_pbh_hash_field_add_ip6_mask(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_dst_ipv6", "--hash-field", "INNER_DST_IPV6",
            "--ip-mask", "ffff::",
            "--sequence-id", "4"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS


    # negative add: --hash-field & --ip-mask mismatch
    def test_config_pbh_hash_field_add_hash_field_with_ip(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_protocol", "--hash-field", "INNER_IP_PROTOCOL",
            "--ip-mask", "255.0.0.0",
            "--sequence-id", "1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    # negative add: --hash-field v6 & --ip-mask v4 mismatch
    def test_config_pbh_hash_field_add_ipv4_mismatch(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv6", "--hash-field", "INNER_SRC_IPV6",
            "--ip-mask", "255.0.0.0",
            "--sequence-id", "4"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    # negative add: --hash-field v4 & --ip-mask v6 mismatch
    def test_config_pbh_hash_field_add_ipv6_mismatch(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv4", "--hash-field", "INNER_SRC_IPV4",
            "--ip-mask", "ffff::",
            "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR

    # negative add: invalid --ip-mask
    def test_config_pbh_hash_field_add_invalid_ip(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv4", "--hash-field", "INNER_SRC_IPV4",
            "--ip-mask", "WRONG",
            "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    # negative add: None --ip-mask
    def test_config_pbh_hash_field_add_none_ipv4(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv4", "--hash-field", "INNER_SRC_IPV4",
            "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    # negative add: None --ip-mask
    def test_config_pbh_hash_field_add_none_ipv6(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_src_ipv6", "--hash-field", "INNER_SRC_IPV6",
            "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    def test_config_pbh_hash_field_update_sequence_id(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["update"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "2"], obj=db)

        assert result.exit_code == SUCCESS


    def test_config_pbh_hash_field_update_hash_field(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["update"],
            ["inner_ip_proto", "--hash-field", "INNER_L4_DST_PORT",
            "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS


    def test_config_pbh_hash_field_update_hash_field_ip_mask(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_dst_ipv4", "--hash-field", "INNER_DST_IPV4",
            "--ip-mask", "255.0.0.0", "--sequence-id", "1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["update"],
            ["inner_dst_ipv4", "--hash-field", "INNER_SRC_IPV4",
            "--ip-mask", "0.0.0.255", "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS


    def test_config_pbh_hash_field_update_wrong_hash_field(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["update"],
            ["inner_ip_proto", "--hash-field", "INNER_DST_IPV4",
            "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    def test_config_pbh_hash_field_update_wrong_ipv4_mask1(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_ip_proto", "--hash-field", "INNER_IP_PROTOCOL",
            "--sequence-id", "1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["update"],
            ["inner_ip_proto", "--ip-mask", "0.0.0.255"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    def test_config_pbh_hash_field_update_wrong_ipv6_mask(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_dst_ipv6", "--hash-field", "INNER_DST_IPV6",
            "--ip-mask", "ffff::", "--sequence-id", "3"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["update"],
            ["inner_dst_ipv6", "--ip-mask", "255.0.0.0", "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    def test_config_pbh_hash_field_update_wrong_ipv4_mask2(self):
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["add"],
            ["inner_dst_ipv4", "--hash-field", "INNER_DST_IPV4",
            "--ip-mask", "255.0.0.0", "--sequence-id", "3"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash-field"].commands["update"],
            ["inner_dst_ipv4", "--ip-mask", "ffff::", "--sequence-id", "2"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)

        assert result.exit_code == ERROR


    ########## CONFIG PBH HASH ##########


    def test_config_pbh_hash_add_delete_ipv4(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'hash_fields')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash"].commands["add"],
            ["inner_v4_hash", "--hash-field-list",
            "inner_ip_proto,inner_l4_dst_port,inner_l4_src_port,inner_dst_ipv4,inner_dst_ipv4"],
            obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash"].commands["delete"],
            ["inner_v4_hash"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS


    def test_config_pbh_hash_add_update_ipv6(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'hash_fields')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash"].commands["add"],
            ["inner_v6_hash", "--hash-field-list",
            "inner_ip_proto,inner_l4_dst_port,inner_l4_src_port,inner_dst_ipv6,inner_dst_ipv6"],
            obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash"].commands["update"],
            ["inner_v6_hash", "--hash-field-list",
            "inner_l4_dst_port,inner_l4_src_port,inner_dst_ipv6,inner_dst_ipv6"],
            obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS


    def test_config_pbh_hash_add_invalid_hash_field_list(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'hash_fields')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash"].commands["add"],
            ["inner_v6_hash", "--hash-field-list",
            "INVALID"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR


    def test_config_pbh_hash_add_empty_hash_field_list(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'hash_fields')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["hash"].commands["add"],
            ["inner_v6_hash", "--hash-field-list",
            ""], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR


    ########## CONFIG PBH TABLE ##########


    def test_config_pbh_table_add_delete_ports(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'table')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["add"],
            ["pbh_table1", "--interface-list", "Ethernet0,Ethernet4",
            "--description", "NVGRE"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["delete"], ["pbh_table1"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS


    def test_config_pbh_table_add_update_portchannels(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'table')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["add"],
            ["pbh_table2", "--interface-list", "PortChannel0001",
            "--description", "VxLAN"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["update"],
            ["pbh_table2", "--interface-list", "PortChannel0002",
            "--description", "VxLAN TEST"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["update"],
            ["pbh_table2", "--interface-list", "PortChannel0001"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["update"],
            ["pbh_table2", "--description", "TEST"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS


    def test_config_pbh_table_add_port_and_portchannel(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'table')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["add"],
            ["pbh_table3", "--interface-list", "PortChannel0002,Ethernet8",
            "--description", "VxLAN adn NVGRE"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS


    def test_config_pbh_table_add_invalid_port(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'table')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["add"],
            ["pbh_table3", "--interface-list", "INVALID",
            "--description", "VxLAN adn NVGRE"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR


    def test_config_pbh_table_add_update_wrong_interface(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'table')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["add"],
            ["pbh_table2", "--interface-list", "PortChannel0001",
            "--description", "VxLAN"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["table"].commands["update"],
            ["pbh_table2", "--interface-list", "INVALID"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR


    ########## CONFIG PBH RULE ##########


    def test_config_pbh_rule_add_delete_nvgre(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "nvgre", "--priority", "1", "--gre-key",
            "0x2500/0xffffff00", "--inner-ether-type", "0x86dd/0xffff",
            "--hash", "inner_v6_hash", "--packet-action", "SET_ECMP_HASH",
            "--flow-counter", "DISABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["delete"], ["pbh_table1", "nvgre"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS


    def test_config_pbh_rule_add_update_vxlan(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "vxlan ", "--priority", "2", "--ip-protocol",
            "0x11/0xff", "--inner-ether-type", "0x0800/0xfff",
            "--l4-dst-port", "0x12b5/0xffff", "--hash", "inner_v4_hash",
            "--packet-action", "SET_LAG_HASH", "--flow-counter", "ENABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["update"],
            ["pbh_table1", "vxlan ", "--priority", "3", "--inner-ether-type", "0x086dd/0xfff",
            "--packet-action", "SET_LAG_HASH", "--flow-counter", "DISABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS


    def test_config_pbh_rule_update_invalid(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "vxlan ", "--priority", "2", "--ip-protocol",
            "0x11/0xff", "--inner-ether-type", "0x0800/0xfff",
            "--l4-dst-port", "0x12b5/0xffff", "--hash", "inner_v6_hash",
            "--packet-action", "SET_ECMP_HASH", "--flow-counter", "ENABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["update"],
            ["pbh_table1", "vxlan ", "--flow-counter", "INVALID"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR2


    def test_config_pbh_rule_add_invalid_ip_priotiry(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "vxlan ", "--priority", "2", "--ip-protocol",
            "INVALID", "--inner-ether-type", "0x0800/0xfff",
            "--l4-dst-port", "0x12b5/0xffff", "--hash", "inner_v6_hash",
            "--packet-action", "SET_ECMP_HASH", "--flow-counter", "ENABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR 


    def test_config_pbh_rule_add_invalid_inner_ether_type(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "vxlan ", "--priority", "2", "--ip-protocol",
            "0x11/0xff", "--inner-ether-type", "INVALID",
            "--l4-dst-port", "0x12b5/0xffff", "--hash", "inner_v6_hash",
            "--packet-action", "SET_ECMP_HASH", "--flow-counter", "ENABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR


    def test_config_pbh_rule_add_invalid_hash(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "vxlan ", "--priority", "2", "--ip-protocol",
            "0x11/0xff", "--inner-ether-type", "0x0800/0xfff",
            "--l4-dst-port", "0x12b5/0xffff", "--hash", "INVALID",
            "--packet-action", "SET_ECMP_HASH", "--flow-counter", "ENABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR


    def test_config_pbh_rule_add_invalid_packet_action(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "vxlan ", "--priority", "2", "--ip-protocol",
            "0x11/0xff", "--inner-ether-type", "0x0800/0xfff",
            "--l4-dst-port", "0x12b5/0xffff", "--hash", "inner_v6_hash",
            "--packet-action", "INVALID", "--flow-counter", "ENABLED"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR2


    def test_config_pbh_rule_add_invalid_flow_counter(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'rule')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(config.config.commands["pbh"].
            commands["rule"].commands["add"],
            ["pbh_table1", "vxlan ", "--priority", "2", "--ip-protocol",
            "0x11/0xff", "--inner-ether-type", "0x0800/0xfff",
            "--l4-dst-port", "0x12b5/0xffff", "--hash", "inner_v6_hash",
            "--packet-action", "SET_ECMP_HASH", "--flow-counter", "INVALID"], obj=db)

        logger.debug(result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR2

    ########## SHOW PBH HASH-FIELD ##########

    def test_show_pbh_hash_field(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'full_pbh_config')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(show.cli.commands["pbh"].
            commands["hash-field"], [], obj=db)

        logger.debug("\n" + result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS
        assert result.output == assert_show_output.show_pbh_hash_fields


    ########## SHOW PBH HASH ##########


    def test_show_pbh_hash(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'full_pbh_config')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(show.cli.commands["pbh"].
            commands["hash"], [], obj=db)

        logger.debug("\n" + result.stdout)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS
        assert result.output == assert_show_output.show_pbh_hash


    ########## SHOW PBH TABLE ##########


    def test_show_pbh_table(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'full_pbh_config')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(show.cli.commands["pbh"].
            commands["table"], [], obj=db)

        logger.debug("\n" + result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS
        assert result.output == assert_show_output.show_pbh_table


    ########## SHOW PBH RULE ##########


    def test_show_pbh_rule(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'full_pbh_config')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(show.cli.commands["pbh"].
            commands["rule"], [], obj=db)

        logger.debug("\n" + result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS
        assert result.output == assert_show_output.show_pbh_rule


    ########## SHOW PBH STATISTICS ##########

    def test_show_pbh_statistics(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'full_pbh_config')
        dbconnector.dedicated_dbs['COUNTERS_DB'] = os.path.join(mock_db_path, 'counters_db')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(show.cli.commands["pbh"].
            commands["statistics"], [], obj=db)

        logger.debug("\n" + result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS
        assert result.output == assert_show_output.show_pbh_statistics

