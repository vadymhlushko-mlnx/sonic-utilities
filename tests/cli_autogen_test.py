import os
import logging
import pprint

import show.plugins as show_plugins

import show.main as show
import config.main as config

from utilities_common import util_base

from sonic_cli_gen.generator import CliGenerator
from click.testing import CliRunner
from utilities_common.db import Db

logger = logging.getLogger(__name__)

test_path = os.path.dirname(os.path.abspath(__file__))
yang_models_path = '/usr/local/yang-models'

show_device_metadata_localhost="""\
HWSKU                   DEFAULT BGP STATUS    DOCKER ROUTING CONFIG MODE    HOSTNAME      PLATFORM                MAC                DEFAULT PFCWD STATUS    BGP ASN      DEPLOYMENT ID  TYPE       BUFFER MODEL    FRR MGMT FRAMEWORK CONFIG
----------------------  --------------------  ----------------------------  ------------  ----------------------  -----------------  ----------------------  ---------  ---------------  ---------  --------------  ---------------------------
Mellanox-SN3800-D112C8  down                  separated                     sonic-switch  x86_64-mlnx_msn3800-r0  1d:34:db:16:a6:00  enable                  N/A                      1  ToRRouter  N/A             N/A
"""

gen = CliGenerator(logger)

class TestCliAutogen:
    @classmethod
    def setup_class(cls):
        logger.info("SETUP")
        os.environ['UTILITIES_UNIT_TESTING'] = "2"
        gen.generate_cli_plugin('show', 'sonic-device_metadata')
        helper = util_base.UtilHelper()
        for plugin in helper.load_plugins(show_plugins):
            helper.register_plugin(plugin, show.cli)

    @classmethod
    def teardown_class(cls):
        logger.info("TEARDOWN")
        gen.remove_cli_plugin('show', 'sonic-device_metadata')
        os.environ['UTILITIES_UNIT_TESTING'] = "0"

    def test_one(self):
        runner = CliRunner()

        result = runner.invoke(show.cli.commands['device-metadata'].commands['localhost'], [])
        logger.debug(result.output)
        assert result.output == show_device_metadata_localhost


