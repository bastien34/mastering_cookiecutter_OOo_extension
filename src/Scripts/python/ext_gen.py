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

COOKIECUTTER_REPO = "https://github.com/bastien34/cookiecutter_ooo_extension"
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

    # Define extra_context (global vars)
    extra_context = {}
    for i, f in enumerate(description_data):
        if i and f[0]:
            extra_context.update({f[0]: f[1]})
    extra_context['extension_name'] = _clean_entry(
        extra_context['extension_name'])

    # Define functions for toolbar and menubar
    funcs = {}
    funcs_attr = ['name', 'label', 'icon']
    for i, f in enumerate(function_data):
        f = list(f)
        if i and f[0]:
            f[0] = _clean_entry(f[0])
            func = dict(zip(funcs_attr, f))
            funcs.update({f[0]: func})

    # Define vars for config.xcs and dialog.xcu
    variables = {}
    option_vars = ('name', 'label', 'type', 'default')
    for i, ov in enumerate(option_data):
        ov = list(ov)
        if i and ov[0]:
            ov[0] = _clean_entry(ov[0])
            var = dict(zip(option_vars, ov))
            variables.update({ov[0]: var})
    extra_context.update({'vars': variables,
                          'funcs': funcs})

    # Launch cookiecutter process. Deactivate overwrite mode in production!
    cookiecutter(COOKIECUTTER_REPO,
                 no_input=True,
                 extra_context=extra_context,
                 overwrite_if_exists=True,
                 checkout='master')


def _clean_entry(v):
    v = v.strip()
    v = v.replace(" ", "_")
    v = v.lower()
    return v


g_exportedScripts = generate_extension_launcher,
