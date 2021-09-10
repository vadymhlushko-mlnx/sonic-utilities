import os
import logging
import pytest

import show.plugins as show_plugins
import show.main as show_main
import config.plugins as config_plugins
import config.main as config_main
from .cli_autogen_input.autogen_test import show_cmd_output
from .cli_autogen_input.cli_autogen_common import backup_yang_models, restore_backup_yang_models

from utilities_common import util_base
from sonic_cli_gen.generator import CliGenerator
from .mock_tables import dbconnector
from utilities_common.db import Db
from click.testing import CliRunner

logger = logging.getLogger(__name__)
gen = CliGenerator(logger)

test_path = os.path.dirname(os.path.abspath(__file__))
mock_db_path = os.path.join(test_path, 'cli_autogen_input')

SUCCESS = 0
ERROR = 1
INVALID_VALUE = 'INVALID'

config_db_path = '/sonic/src/sonic-utilities/tests/cli_autogen_input/config_db.json'
templates_path = '/sonic/src/sonic-utilities/sonic-utilities-data/templates/sonic-cli-gen/'


class TestCliAutogen:
    @classmethod
    def setup_class(cls):
        logger.info('SETUP')
        os.environ['UTILITIES_UNIT_TESTING'] = "2"

        backup_yang_models()

        gen.generate_cli_plugin(
            cli_group='show',
            plugin_name='sonic-device_metadata',
            config_db_path=config_db_path,
            templates_path=templates_path
        )
        gen.generate_cli_plugin(
            cli_group='config',
            plugin_name='sonic-device_metadata',
            config_db_path=config_db_path,
            templates_path=templates_path
        )

        helper = util_base.UtilHelper()
        helper.load_and_register_plugins(show_plugins, show_main.cli)
        helper.load_and_register_plugins(config_plugins, config_main.config)


    @classmethod
    def teardown_class(cls):
        logger.info('TEARDOWN')

        gen.remove_cli_plugin('show', 'sonic-device_metadata')
        gen.remove_cli_plugin('config', 'sonic-device_metadata')

        restore_backup_yang_models()

        dbconnector.dedicated_dbs['CONFIG_DB'] = None

        os.environ['UTILITIES_UNIT_TESTING'] = "0"


    def test_show_device_metadata(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'config_db')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(
            show_main.cli.commands['device-metadata'].commands['localhost'], [], obj=db
        )

        logger.debug("\n" + result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS
        assert result.output == show_cmd_output.show_device_metadata_localhost


    def test_config_device_metadata(self):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'config_db')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(
            config_main.config.commands['device-metadata'].commands['localhost'].commands['buffer-model'], ['dynamic'], obj=db
        )

        result = runner.invoke(
            show_main.cli.commands['device-metadata'].commands['localhost'], [], obj=db
        )

        logger.debug("\n" + result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == SUCCESS
        assert result.output == show_cmd_output.show_device_metadata_localhost_changed_buffer_model


    @pytest.mark.parametrize("parameter,value", [
        ('default-bgp-status', INVALID_VALUE),
        ('docker-routing-config-mode', INVALID_VALUE),
        ('mac', INVALID_VALUE),
        ('default-pfcwd-status', INVALID_VALUE),
        ('bgp-asn', INVALID_VALUE),
        ('type', INVALID_VALUE),
        ('buffer-model', INVALID_VALUE),
        ('frr-mgmt-framework-config', INVALID_VALUE)
    ])
    def test_config_device_metadata_invalid(self, parameter, value):
        dbconnector.dedicated_dbs['CONFIG_DB'] = os.path.join(mock_db_path, 'config_db')
        db = Db()
        runner = CliRunner()

        result = runner.invoke(
            config_main.config.commands['device-metadata'].commands['localhost'].commands[parameter], [value], obj=db
        )

        logger.debug("\n" + result.output)
        logger.debug(result.exit_code)
        assert result.exit_code == ERROR

