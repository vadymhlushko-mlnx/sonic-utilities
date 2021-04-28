#!/usr/bin/env python

try:
    import sys
    import os
    import click
    from sonic_cli_gen.generator import CliGenerator
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

@click.group()
@click.pass_context
def cli(ctx):
    """ SONiC CLI generator """
    print ("cli")
    pass

@cli.command()
@click.pass_context
def generate_config(ctx):
    """ List available packages """
    gen = CliGenerator('sonic-flex_counter')
    gen.generate_config_plugin()
    pass

if __name__ == '__main__':
    cli()