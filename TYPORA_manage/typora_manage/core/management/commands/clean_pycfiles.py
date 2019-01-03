#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os


from typora_manage.utils.logger import Logger
from typora_manage.core.management.base import BaseCommand


logger = Logger().get_logger(__name__)


class Command(BaseCommand):
    help = 'Auto clean pyc file in typaro project'

    def __init__(self):
        super(Command, self).__init__()

    def add_parser_arguments(self, parser):
        parser.add_argument('-p', dest='path', help='typaro notes root directory', type=str, required=True)

    @staticmethod
    def _is_valid_pycfile(path):
        if not path.endswith('.pyc') or os.path.basename(path).count('.') != 1:
            logger.debug('Invalid pyc file ({0}), ignore{1}'.format(path, os.linesep))
            return False
        return True

    def handle(self, *args, **kwargs):
        for root, dirs, files in os.walk(kwargs.get('path'), topdown=True, onerror=None, followlinks=False):
            for f in files:
                f_path = os.path.join(root, f)
                if not self._is_valid_pycfile(f_path):
                    continue
                logger.warning('Found unused pycfile({0}) in {1}, deleted'.format(f, root))
                os.remove(f_path)
