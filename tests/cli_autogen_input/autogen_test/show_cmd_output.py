"""
Module holding correct output for the show command for cli_autogen_test.py
"""


show_device_metadata_localhost="""\
HWSKU        DEFAULT BGP STATUS    DOCKER ROUTING CONFIG MODE    HOSTNAME    PLATFORM                MAC                DEFAULT PFCWD STATUS    BGP ASN    DEPLOYMENT ID    TYPE       BUFFER MODEL    FRR MGMT FRAMEWORK CONFIG
-----------  --------------------  ----------------------------  ----------  ----------------------  -----------------  ----------------------  ---------  ---------------  ---------  --------------  ---------------------------
ACS-MSN2100  up                    N/A                           r-sonic-01  x86_64-mlnx_msn2100-r0  ff:ff:ff:ff:ff:00  disable                 N/A        N/A              ToRRouter  traditional     N/A
"""

show_device_metadata_localhost_changed_buffer_model="""\
HWSKU        DEFAULT BGP STATUS    DOCKER ROUTING CONFIG MODE    HOSTNAME    PLATFORM                MAC                DEFAULT PFCWD STATUS    BGP ASN    DEPLOYMENT ID    TYPE       BUFFER MODEL    FRR MGMT FRAMEWORK CONFIG
-----------  --------------------  ----------------------------  ----------  ----------------------  -----------------  ----------------------  ---------  ---------------  ---------  --------------  ---------------------------
ACS-MSN2100  up                    N/A                           r-sonic-01  x86_64-mlnx_msn2100-r0  ff:ff:ff:ff:ff:00  disable                 N/A        N/A              ToRRouter  dynamic         N/A
"""

show_device_neighbor="""\
PEER NAME    NAME      MGMT ADDR    LOCAL PORT    PORT    TYPE
-----------  --------  -----------  ------------  ------  ------
Ethernet0    Servers   10.217.0.1   Ethernet0     eth0    type
Ethernet4    Servers0  10.217.0.2   Ethernet4     eth1    type
"""

show_device_neighbor_added="""\
PEER NAME    NAME      MGMT ADDR    LOCAL PORT    PORT    TYPE
-----------  --------  -----------  ------------  ------  ------
Ethernet0    Servers   10.217.0.1   Ethernet0     eth0    type
Ethernet4    Servers0  10.217.0.2   Ethernet4     eth1    type
Ethernet8    Servers1  10.217.0.3   Ethernet8     eth2    type
"""


show_device_neighbor_deleted="""\
PEER NAME    NAME      MGMT ADDR    LOCAL PORT    PORT    TYPE
-----------  --------  -----------  ------------  ------  ------
Ethernet4    Servers0  10.217.0.2   Ethernet4     eth1    type
"""