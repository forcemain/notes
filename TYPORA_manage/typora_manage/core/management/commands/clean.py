#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os


from typora_manage.utils.pipe import Pipe
from typora_manage.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Auto clean unused typaro assets images'

    def __init__(self):
        super(Command, self).__init__()

    def add_parser_arguments(self, parser):
        parser.add_argument('-p', dest='path', help='typaro notes root directory', type=str, required=True)

    def _is_valid_assets(self, root, name):
        d_path = os.path.join(root, name)
        if not os.path.exists(d_path):
            self.stderr.write('Invalid markdown dirs ({0}), ignore{1}'.format(d_path, os.linesep))
            return False
        return True

    def _is_valid_mdfile(self, root, name):
        f_path = os.path.join(root, name)
        if not name.endswith('.md') or name.count('.') != 1:
            self.stderr.write('Invalid markdown file ({0}), ignore{1}'.format(f_path, os.linesep))
            return False
        return True

    def _get_markdown_images(self):
        return []

    def _del_unused_images(self):
        return []

    def handle(self, *args, **kwargs):
        for root, dirs, files in os.walk(kwargs.get('path'), topdown=True, onerror=None, followlinks=False):
            for f in files:
                if not self._is_valid_mdfile(root, f):
                    continue
                f_name, _, f_suffix = f.rpartition('.')
                d_name = '{0}.{1}'.format(f_name, 'assets')
                if not self._is_valid_assets(root, d_name):
                    continue
                f_path = os.path.join(root, f)
                d_path = os.path.join(root, d_name)

                Pipe(self._get_markdown_images)|Pipe(self._del_unused_images)