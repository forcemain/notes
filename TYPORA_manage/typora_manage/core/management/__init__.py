#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import sys
import pkgutil
import importlib


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

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'

        self.fetch_command(subcommand).run_from_argv(self.argv)

    def fetch_command(self, subcommand):
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            print 'Unknow command: {0}{1}Type "{2} help" for usage'.format(
                subcommand, os.linesep, self.prog_name
            )
            sys.exit(1)
        klass = load_command_class(app_name, subcommand)
        return klass


def execute_from_command_line(argv=None):
    management = Management(argv)
    management.execute()
