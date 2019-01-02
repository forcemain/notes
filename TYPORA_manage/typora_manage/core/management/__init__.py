#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import sys
import pkgutil
import importlib


from collections import OrderedDict


def find_commands(management_dir):
    command_dir = os.path.join(management_dir, 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def get_commands():
    commands = {name: 'typora_manage.core' for name in find_commands(__path__[0])}

    return commands


def load_command_class(app_name, name):
    module = importlib.import_module('{0}.management.commands.{1}'.format(app_name, name))
    return module.Command()


class Management(object):
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def main_help_text(self):
        usage = [
            "",
            "Type '%s <subcommand> -h or --help' for help on a specific subcommand." % self.prog_name,
            "",
            "Available subcommands:",
        ]
        available_dict = OrderedDict()
        commands = get_commands()
        for name in commands:
            app_name = commands[name]
            available_dict.setdefault(app_name, []).append(name)
        print os.linesep.join(usage)
        for name in available_dict:
            print '[ {0} ]'.format(name)
            print os.linesep.join(available_dict[name])

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = '--help'

        if subcommand in ['-h', '--help']:
            self.main_help_text()
            sys.exit(0)

        self.fetch_command(subcommand).run_from_argv(self.argv)

    def fetch_command(self, subcommand):
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            print 'Unknow command: {0}{1}Type "{2} -h or --help" for usage'.format(
                subcommand, os.linesep, self.prog_name
            )
            sys.exit(1)
        klass = load_command_class(app_name, subcommand)
        return klass


def execute_from_command_line(argv=None):
    management = Management(argv)
    management.execute()
