import sys
import os
from click.testing import CliRunner

test_path = os.path.dirname(os.path.abspath(__file__))
modules_path = os.path.dirname(test_path)
scripts_path = os.path.join(modules_path, "scripts")
sys.path.insert(0, test_path)
sys.path.insert(0, modules_path)

import mock_tables.dbconnector
import show.main as show 

expected_rates = """    IFACE    STATE    RX_OK        RX_BPS     RX_PPS    RX_UTIL    TX_OK       TX_BPS     TX_PPS    TX_UTIL
---------  -------  -------  ------------  ---------  ---------  -------  -----------  ---------  ---------
Ethernet0        D      N/A      0.00 B/s     0.00/s      0.00%      N/A     0.00 B/s     0.00/s      0.00%
Ethernet4      N/A      N/A   200.00 KB/s   200.00/s      0.00%      N/A  200.05 KB/s   201.00/s      0.00%
Ethernet8      N/A      N/A  1318.36 KB/s  9000.00/s      0.03%      N/A   12.75 MB/s  9000.00/s      0.25%
"""


class TestRates(object):
    @classmethod
    def setup_class(cls):
        print("SETUP")
        os.environ["PATH"] += os.pathsep + scripts_path
        os.environ["UTILITIES_UNIT_TESTING"] = "1"

    def test_rates(self):
        runner = CliRunner()
        result = runner.invoke(show.cli.commands["interfaces"].commands["counters"].commands["rates"], [])
        print(result.output)
        assert result.output == expected_rates

    @classmethod
    def teardown_class(cls):
        print("TEARDOWN")
        os.environ["PATH"] = os.pathsep.join(os.environ["PATH"].split(os.pathsep)[:-1])
        os.environ["UTILITIES_UNIT_TESTING"] = "0"
