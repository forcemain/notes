#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import sys


from argparse import ArgumentParser


class BaseCommand(object):
    help = ''

    def __init__(self, stdout=None, stderr=None):
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

    def create_parser(self, prog_name, subcommand):
        parser = ArgumentParser(
            prog='{0} {1}'.format(prog_name, subcommand), description=self.help or None
        )
        self.add_parser_arguments(parser)

        return parser

    def add_parser_arguments(self, parser):
        pass

    def print_help(self, prog_name, subcommand):
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv=None):
        parser = self.create_parser(os.path.basename(argv[0]), argv[1])
        kwargs = vars(parser.parse_args(argv[2:]))

        # do something
        args = kwargs.pop('args', [])

        self.handle(*args, **kwargs)

    def handle(self, *args, **kwargs):
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
