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
    pass

@cli.command()
@click.argument('yang_model_name')
@click.pass_context
def generate_config(ctx, yang_model_name):
    """ Generate config plugin """
    gen = CliGenerator(yang_model_name)
    gen.generate_config_plugin()
    pass

if __name__ == '__main__':
    cli()