#!/usr/bin/env python

import click
from sonic_cli_gen.generator import CliGenerator

@click.group()
@click.pass_context
def cli(ctx):
    """ SONiC CLI Auto-generator tool.\r
        Generate click CLI plugin for 'config' or 'show' CLI groups.\r
        CLI plugin will be generated from the YANG model, which should be in:\r\n
        /usr/local/yang-models/ \n
        Generated CLI plugin will be placed in: \r\n
        /usr/local/lib/python3.7/dist-packages/<CLI group>/plugins/auto/
    """

    context = {
        'gen': CliGenerator()
    }
    ctx.obj = context


@cli.command()
@click.argument('cli_group', type = click.Choice(['config', 'show']))
@click.argument('yang_model_name', type = click.STRING)
@click.pass_context
def generate(ctx, cli_group, yang_model_name):
    """ Generate click CLI plugin. """

    ctx.obj['gen'].generate_cli_plugin(cli_group = cli_group, plugin_name = yang_model_name)


@cli.command()
@click.argument('cli_group', type = click.Choice(['config', 'show']))
@click.argument('yang_model_name', type = click.STRING)
@click.pass_context
def remove(ctx, cli_group, yang_model_name):
    """ Remove generated click CLI plugin from. """

    ctx.obj['gen'].remove_cli_plugin(cli_group = cli_group, plugin_name = yang_model_name)


if __name__ == '__main__':
    cli()

