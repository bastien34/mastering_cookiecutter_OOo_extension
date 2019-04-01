#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging.config
import xml.etree.ElementTree as ET
from _elementtree import Element

import yaml
from helpers import (ElemProp, Elem)


# General
# extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"

xml_file = "{{cookiecutter.extension_name}}_config.xcs"
locale = {"xml:lang": "fr"}

logger = logging.getLogger(__name__)


def create_config_xcs(option_vars, temp_dir):
    """
    Creation of OptionsDialog.xcu.

    This file contains description of option vars values.

    Its parameter is a list of Var Instance.
    """
    path_file = os.path.join(temp_dir, xml_file)

    logger.debug('Start creating %s.', path_file)

    root = Element("oor:component-schema",
                   {"xmlns:oor": "http://openoffice.org/2001/registry",
                    "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
                    "oor:name": "ExtensionData",
                    "oor:package": "{{cookiecutter.package_name}}",
                    "xml:lang": "en-US"})

    with open(path_file, "w", encoding="UTF-8") as xf:
        template = ET.SubElement(root, "templates")
        group = ET.SubElement(template, 'group', {'oor:name': "Production"})
        inf = ET.SubElement(group, 'info')
        inf.append(Elem('desc', {'text': 'Values for production mode'}))
        defaults = ET.SubElement(group, 'group', {'oor:name': 'Defaults'})

        # Iteration on options list
        for ov in option_vars:
            vtype = f'xs:{ov.vtype}'
            ET.SubElement(group, 'prop', {'oor:name': ov.name,
                                          'oor:type': vtype})
            defaults.append(ElemProp(ov.name, ov.default,
                                     {'oor:type': vtype}))

        # Component
        cmp = ET.SubElement(root, 'component')
        leaves = ET.SubElement(cmp, 'group', {'oor:name': 'Leaves'})
        leaves.append(
            Elem('node-ref', {'oor:name': "{{cookiecutter.extension_name}}",
                              'oor:node-type': "Production"}))

        tree = ET.ElementTree(root)
        tree.write(xf.name, "utf-8", True)

    logger.info("%s created in -> %s", xml_file, temp_dir)


if __name__ == "__main__":
    with open('logging_conf.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(log_cfg)
