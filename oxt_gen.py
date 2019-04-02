#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
import shutil

version = '0.0.1'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('zip_generator')
file_name = f"extension_generator{version}_local.odt"


def zip_files():
    msg = f'Zipping Extension generator {version}'
    logger.info(msg)
    file_path = os.path.join('../temp', file_name)
    shutil.make_archive(file_path, 'zip', 'src/')
    os.rename(file_path + '.zip', file_path)
    logger.info(f'zib has been made in: {file_path}')
    return 1


if __name__ == '__main__':
    zip_files()
