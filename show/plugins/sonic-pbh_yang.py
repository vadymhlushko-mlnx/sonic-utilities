"""
Auto-generated show CLI plugin.
"""

import click
import tabulate
import natsort
import utilities_common.cli as clicommon

def format_attr_value(entry, attr):
    """ Helper that formats attribute to be presented in the table output.

    Args:
        entry (Dict[str, str]): CONFIG DB entry configuration.
        attr (Dict): Attribute metadata.

    Returns:
        str: fomatted attribute value.
    """

    if attr["is-leaf-list"]:
        return "\n".join(entry.get(attr["name"], []))
    return entry.get(attr["name"], "N/A")

def format_group_value(entry, attrs):
    """ Helper that formats grouped attribute to be presented in the table output.

    Args:
        entry (Dict[str, str]): CONFIG DB entry configuration.
        attrs (List[Dict]): Attributes metadata that belongs to the same group.

    Returns:
        str: fomatted group attributes.
    """

    data = []
    for attr in attrs:
        if entry.get(attr["name"]):
            data.append((attr["name"] + ":", format_attr_value(entry, attr)))
    return tabulate.tabulate(data, tablefmt="plain")

@click.group(name="pbh-hash",
             cls=clicommon.AliasedGroup,
             invoke_without_command=True)
@clicommon.pass_db
def PBH_HASH(db):
    """  [Callable command group] """

    header = [
        "HASH NAME",
        "HASH FIELD",
        "IPV4 MASK",
        "IPV6 MASK",
        "SEQUENCE ID",
    ]

    body = []

    table = db.cfgdb.get_table("PBH_HASH")
    for key in natsort.natsorted(table):
        entry = table[key]
        if not isinstance(key, tuple):
            key = (key,)

        row = [*key] + [
            format_attr_value(
                entry,
                {'name': 'hash_field',
                 'description': 'Configures native hash field for this hash',
                 'is-leaf-list': False,
                 'is-mandatory': True,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'ipv4_mask',
                 'description': 'Configures IPv4 address mask for this hash',
                 'is-leaf-list': False,
                 'is-mandatory': True,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'ipv6_mask',
                 'description': 'Configures IPv6 address mask for this hash',
                 'is-leaf-list': False,
                 'is-mandatory': True,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'sequence_id',
                 'description': 'Configures in which order the fields are hashed and defines which fields should be associative',
                 'is-leaf-list': False, 
                 'is-mandatory': True,
                 'group': ''}
            ),
        ]

    body.append(row)
    click.echo(tabulate.tabulate(body, header))


@click.group(name="pbh-rule",
             cls=clicommon.AliasedGroup,
             invoke_without_command=True)
@clicommon.pass_db
def PBH_RULE(db):
    """  [Callable command group] """

    header = [
        "TABLE NAME",
        "RULE NAME",
        "PRIORITY",
        "GRE KEY",
        "IP PROTOCOL",
        "IPV6 NEXT HEADER",
        "L4 DST PORT",
        "INNER ETHER TYPE",
        "PACKET ACTION",
        "FLOW COUNTER",
        "HASH LIST",
    ]

    body = []

    table = db.cfgdb.get_table("PBH_RULE")
    for key in natsort.natsorted(table):
        entry = table[key]
        if not isinstance(key, tuple):
            key = (key,)

        row = [*key] + [
            format_attr_value(
                entry,
                {'name': 'priority',
                 'description': 'Configures priority for this rule',
                 'is-leaf-list': False,
                 'is-mandatory': True,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'gre_key',
                 'description': 'Configures packet match for this rule: GRE key',
                 'is-leaf-list': False,
                 'is-mandatory': False, 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'ip_protocol',
                 'description': 'Configures packet match for this rule: IP protocol',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'ipv6_next_header',
                 'description': 'Configures packet match for this rule: IPv6 Next header',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'l4_dst_port',
                 'description':'Configures packet match for this rule: L4 destination port',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'inner_ether_type',
                 'description': 'Configures packet match for this rule: inner EtherType',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'packet_action',
                 'description': 'Configures packet action for this rule',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'flow_counter',
                 'description': 'Enables/Disables packet/byte counter for this rule',
                 'is-leaf-list': False,
                 'is-mandatory': False,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'hash_list',
                 'description': 'The list of hash fields to apply with this rule',
                 'is-leaf-list': True,
                 'is-mandatory': False,
                 'group': ''}
            ),
        ]

    body.append(row)
    click.echo(tabulate.tabulate(body, header))


@click.group(name="pbh-table",
             cls=clicommon.AliasedGroup,
             invoke_without_command=True)
@clicommon.pass_db
def PBH_TABLE(db):
    """  [Callable command group] """

    header = [
        "TABLE NAME",
        "DESCRIPTION",
        "INTERFACE LIST",
    ]

    body = []

    table = db.cfgdb.get_table("PBH_TABLE")
    for key in natsort.natsorted(table):
        entry = table[key]
        if not isinstance(key, tuple):
            key = (key,)

        row = [*key] + [
            format_attr_value(
                entry,
                {'name': 'description',
                 'description': 'The description of this table',
                 'is-leaf-list': False,
                 'is-mandatory': True,
                 'group': ''}
            ),
            format_attr_value(
                entry,
                {'name': 'interface_list',
                 'description': 'Interfaces to which this table is applied',
                 'is-leaf-list': True,
                 'is-mandatory': False,
                 'group': ''}
            ),
        ]

    body.append(row)
    click.echo(tabulate.tabulate(body, header))


def register(cli):
    cli_node = PBH_HASH
    if cli_node.name in cli.commands:
        raise Exception(f"{cli_node.name} already exists in CLI")
    cli.add_command(PBH_HASH)
    cli_node = PBH_RULE
    if cli_node.name in cli.commands:
        raise Exception(f"{cli_node.name} already exists in CLI")
    cli.add_command(PBH_RULE)
    cli_node = PBH_TABLE
    if cli_node.name in cli.commands:
        raise Exception(f"{cli_node.name} already exists in CLI")
    cli.add_command(PBH_TABLE)
