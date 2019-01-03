#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import re
import glob


from typora_manage.utils.logger import Logger
from typora_manage.core.management.base import BaseCommand


images_suffix = 'png'
logger = Logger().get_logger(__name__)
images_pattern = re.compile(r'image-[0-9-]+.{0}'.format(images_suffix))


class Command(BaseCommand):
    help = 'Auto clean unused typaro assets images'

    def __init__(self):
        super(Command, self).__init__()

    def add_parser_arguments(self, parser):
        parser.add_argument('-p', dest='path', help='typaro notes root directory', type=str, required=True)

    @staticmethod
    def _is_valid_assets(path):
        if not os.path.exists(path):
            logger.debug('Invalid markdown dirs ({0}), ignore{1}'.format(path, os.linesep))
            return False
        return True

    @staticmethod
    def _is_valid_mdfile(path):
        if not path.endswith('.md') or os.path.basename(path).count('.') != 1:
            logger.debug('Invalid markdown file ({0}), ignore{1}'.format(path, os.linesep))
            return False
        return True

    @staticmethod
    def _get_mdused_images(path):
        images = set()
        with open(path) as f:
            for line in f:
                images.update(re.findall(images_pattern, line))
        return images

    @staticmethod
    def _del_unused_images(path, mdused_images):
        path_old = os.getcwdu()

        os.chdir(path)
        images = set(glob.glob('*.{0}'.format(images_suffix)))
        for img in images.difference(mdused_images):
            logger.warning('Found unused image({0}) in {1}, deleted'.format(img, path))
            os.remove(img)
        os.chdir(path_old)

    def handle(self, *args, **kwargs):
        for root, dirs, files in os.walk(kwargs.get('path'), topdown=True, onerror=None, followlinks=False):
            for f in files:
                f_path = os.path.join(root, f)
                if not self._is_valid_mdfile(f_path):
                    continue
                f_name, _, f_suffix = f.rpartition('.')
                d_name = '{0}.{1}'.format(f_name, 'assets')
                d_path = os.path.join(root, d_name)
                if not self._is_valid_assets(d_path):
                    continue
                mdused_images = self._get_mdused_images(f_path)
                self._del_unused_images(d_path, mdused_images)
