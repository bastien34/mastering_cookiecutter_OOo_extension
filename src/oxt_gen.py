#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import shutil

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('post_gen_project')
extension_name = "ext_gen-0.0.1.oxt"


def zip_files():
    msg = 'Zipping file to %s' % extension_name
    logger.info(msg)
    extension_path = 'extension/'
    oxt = os.path.join(extension_path, extension_name)
    shutil.make_archive(oxt, 'zip', 'src/')
    os.rename(oxt + '.zip', oxt)
    return 1


if __name__ == '__main__':
    zip_files()
