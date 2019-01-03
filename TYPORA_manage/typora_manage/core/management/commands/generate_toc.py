#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import re
import sys


from typora_manage.utils.logger import Logger
from typora_manage.core.management.base import BaseCommand


logger = Logger().get_logger(__name__)
mdcode_pattern = re.compile(r'``?`?`?[^`]+``?`?`?')
titles_pattern = re.compile('^(?P<sharp>##?#?#?)(?P<title>[^#]+)$')


class Command(BaseCommand):
    help = 'Auto generate gfm-toc for a specific markdown file'

    def __init__(self):
        super(Command, self).__init__()

    def add_parser_arguments(self, parser):
        parser.add_argument('-p', dest='path', help='markdown file path', type=str, required=True)

    @staticmethod
    def _is_valid_mdfile(path):
        if not path.endswith('.md') or os.path.basename(path).count('.') != 1:
            logger.debug('Invalid markdown file ({0}), ignore{1}'.format(path, os.linesep))
            return False
        return True

    @staticmethod
    def _gen_markdown_toc(path):
        with open(path) as f:
            with_close_nu = 0
            for line in f:
                match = mdcode_pattern.search(line)
                if match:
                    continue
                if '`' in line:
                    with_close_nu += 1
                    continue
                if 0 < with_close_nu < 2:
                    continue
                else:
                    with_close_nu = 0
                match = titles_pattern.search(line)
                if not match:
                    continue
                sharp, title = match.groupdict().values()
                title_toc_strip = title.strip()
                sharp_toc_ljust = (len(sharp)-1)*2
                print '{0} [{1}](#{1})'.format('{0}*'.format(sharp_toc_ljust*' '), title_toc_strip)

    def handle(self, *args, **kwargs):
        f_path = kwargs.get('path')
        if not self._is_valid_mdfile(f_path):
            sys.exit(1)
        self._gen_markdown_toc(f_path)
