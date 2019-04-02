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

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException

COOKIECUTTER_REPO = "https://github.com/bastien34/cookiecutter_ooo_extension"
module = "{{cookiecutter.extension_name}}"
extension_filename = "{{cookiecutter.extension_name}}-{{cookiecutter.extension_version}}.oxt"


def generate_extension_launcher(*args):

    # We get values from configuration tables
    doc = XSCRIPTCONTEXT.getDocument()
    tb = doc.getTextTables().getByName('description_table')
    description_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('function_table')
    function_data = tb.getDataArray()
    tb = doc.getTextTables().getByName('option_table')
    option_data = tb.getDataArray()

    # Define functions for toolbar and menubar
    extra_context_funcs = []
    funcs = ['name', 'label', 'icon']
    for i, f in enumerate(function_data):
        if i and f[0]:
            func = dict(zip(funcs, f))
            func.update({'module': module})
            extra_context_funcs.append(func)

    # Define vars for config.xcs and dialog.xcu
    extra_context_vars = []
    option_vars = ['name', 'label', 'type', 'default']
    for i, ov in enumerate(option_data):
        if i and ov[0]:
            var = dict(zip(option_vars, ov))
            extra_context_vars.append(var)

    # Define extra_context (global vars)
    extra_context_description = {}
    [extra_context_description.update({r[0]: r[1]}) for r in description_data]

    # Define the output directory and launch cookiecutter process
    try:
        cookiecutter(COOKIECUTTER_REPO,
                     no_input=True,
                     extra_context={'description': extra_context_description,
                                    'funcs': extra_context_funcs,
                                    'vars': extra_context_vars}, )
    except OutputDirExistsException:
        print("Extension already exists. Remove it and start again!")


g_exportedScripts = generate_extension_launcher,
