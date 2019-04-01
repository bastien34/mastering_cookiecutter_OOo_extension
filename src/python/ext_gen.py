# -*- coding: utf-8 -*-

#  grh_mail.py
#
#  Copyright 2019 Bastien Roques <bastien.roques1@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

"""
update unopkg:
cp -r src/python/* ~/.config/libreoffice/4/user/uno_packages/cache/uno_packages/lu29198y6r5iy.tmp_/extension_generator_launcher-0.0.1.oxt/python/
"""

from com.sun.star.beans import PropertyValue
from config_xcs import create_config_xcs
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from create_addon_ui import create_addon
from dialog import create_dialog

from ext_gen_utils import (
    msgbox,
    mri,
    get_config,
    get_package_path,
)
from ext_gen.options_dialog import NODE, KEYS


COOKIECUTTER_REPO = "https://github.com/bastien34/cookiecutter_ooo_extension"
module = "{{cookiecutter.extension_name}}"
extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"
temp_dir = '/tmp/ext_gen'


class Environ:
    """
    Supply environment keys.
        eg: env = Environ()
            my_url = env.URL
    """

    def __init__(self):
        self.node = NODE
        self.keys = KEYS
        self.settings = get_config(self.node, self.keys)

    @property
    def output_dir(self):
        return self.settings.get('output_dir')


class Function:
    """
    Define a function, which is used in AddonUi creation for building
    toolbar and menubar.

    Warning: Location attribute contains an ampersand "&" that must
    be converted as "&amp;" in xml file.
    """

    def __init__(self, name, label, icon):
        self.name = name
        self.label = label
        self.icon = icon

    @property
    def location(self):
        return f"vnd.sun.star.script:{extension_filename}|python" \
            f"|{module}.py${self.name}?language=Python&location=user:" \
            f"uno_packages"


class Var:
    """
    Var instances are part of config.xcs and dialog creation.
    """
    def __init__(self, name, label, vtype, default):
        self.name = name
        self.label = label
        self.vtype = vtype
        self.default = default


def ext_gen_launcher(*args):
    """
    Launcher for creating a MissionBal2Word document.
    """
    print('Extension generation launcher called!')
    desktop = XSCRIPTCONTEXT.getDesktop()
    args = (PropertyValue('Hidden', 0, False, 0),)
    path = '../../_configurator.odt'
    gpp = get_package_path(path)
    return desktop.loadComponentFromURL(
        gpp, "_default", 0, args)


def generate_extension_launcher(*args):
    print('starting...')

    # We get values from configuration tables
    doc = XSCRIPTCONTEXT.getDocument()
    tb = doc.getTextTables().getByName('description_table')
    description_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('function_table')
    function_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('option_table')
    option_data = tb.getDataArray()

    # Define functions for toolbar and menubar
    funcs = []
    for i, o in enumerate(function_data):
        if i and o[0]:
            funcs.append(Function(*o))
    create_addon(funcs, temp_dir)

    # Define vars for config.xcs and dialog.xcu
    vars = []
    for i, o in enumerate(option_data):
        if i and o[0]:
            vars.append(Var(*o))
    create_config_xcs(vars, temp_dir)

    # Create DialogBox
    create_dialog(vars, temp_dir)

    # Define extra_context (global vars)
    extra_context = {}
    [extra_context.update({r[0]: r[1]}) for r in description_data]

    # Define the output directory and launch cookiecutter process
    env = Environ()
    output_dir = env.output_dir
    try:
        cookiecutter(COOKIECUTTER_REPO,
                     no_input=True,
                     extra_context=extra_context,
                     output_dir=output_dir)
    except OutputDirExistsException:
        msgbox("Extension already exists. Remove it and start again!")


g_exportedScripts = ext_gen_launcher, generate_extension_launcher,
