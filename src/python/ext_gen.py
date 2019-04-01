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
from cookiecutter.main import cookiecutter

from ext_gen_utils import (
    msgbox,
    mri,
    get_config,
    get_package_path,
)
from ext_gen.options_dialog import NODE, KEYS

COOKIECUTTER_REPO = "https://github.com/bastien34/cookiecutter_ooo_extension"


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
    msgbox('starting...')

    # We get values from configuration tables
    doc = XSCRIPTCONTEXT.getDocument()
    tb = doc.getTextTables().getByName('description_table')
    description_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('function_table')
    function_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('option_table')
    option_data = tb.getDataArray()

    # Define the output directory
    env = Environ()
    output_dir = env.output_dir

    # Define extra_context (global vars)
    extra_context = {}
    [extra_context.update({r[0]: r[1]}) for r in description_data]

    # Launch cookiecutter process
    cookiecutter(COOKIECUTTER_REPO,
                 no_input=True,
                 extra_context=extra_context,
                 output_dir=output_dir)


g_exportedScripts = ext_gen_launcher, generate_extension_launcher,
