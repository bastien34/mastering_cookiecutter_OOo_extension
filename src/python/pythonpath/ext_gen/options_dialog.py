# -*- coding: utf-8 -*-

import os
import uno
import locale
import gettext
from urllib.parse import urlparse
import unohelper
from com.sun.star.awt import (
    XContainerWindowEventHandler,
    XActionListener,
)
from com.sun.star.lang import XServiceInfo

import traceback

from ext_gen_utils import (
    mri,
    msgbox,
    getConfigurationAccess,
)

DIALOG_ID = 'ext_gen_dialog'
NODE = "com.palaceweb.ext_gen.ExtensionData/Leaves/ext_gen"

KEYS = ("output_dir", )


def create(ctx, implementation_name, service_name, *args):
    global IMPLEMENTATION_NAME
    global SERVICE_NAME
    IMPLEMENTATION_NAME = implementation_name
    SERVICE_NAME = service_name
    try:
        localization()
    except Exception as e:
        traceback.print_exc()

    return DialogHandler(ctx, *args)


def localization():
    wd = urlparse(os.path.dirname(__file__)).path
    locale_dir = os.path.join(wd, "../locales")
    lang, enc = locale.getlocale()
    t = gettext.translation(domain='messages',
                            localedir=locale_dir,
                            languages=[lang])
    t.install()


class DialogBase(object):
    """ Base class for dialog. """
    def __init__(self, ctx):
        self.ctx = ctx
        self.smgr = ctx.getServiceManager()

    def create(self, name, arguments=None):
        """ Create service instance. """
        if arguments:
            return self.smgr.createInstanceWithArgumentsAndContext(
                name, arguments, self.ctx)
        else:
            return self.smgr.createInstanceWithContext(
                name, self.ctx)


class DialogHandler(unohelper.Base, XServiceInfo, XContainerWindowEventHandler):
    """Main class. Dialog handler."""

    METHOD_NAME = "external_event"

    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.cfg_names = KEYS
        self.cfg_nodes = NODE

    def callHandlerMethod(self, dialog, event_name, method_name):
        """XContainerWindowEventHandler"""
        if method_name == self.METHOD_NAME:
            try:
                self._handle_external_event(dialog, event_name)
            except:
                traceback.print_exc()

    def _handle_external_event(self, dialog, event_name):
        if event_name == "ok":
            self._save_data(dialog)
        elif event_name == "back":
            self._load_data(dialog, "back")
        elif event_name == "initialize":
            self._load_data(dialog, "initialize")

    def _save_data(self, dialog):
        assert dialog.getModel().Name == DIALOG_ID
        settings = {}
        for name in self.cfg_names:
            ctrl = dialog.getControl(name)
            if ctrl.supportsService("com.sun.star.awt.UnoControlCheckBox"):
                settings[name] = ctrl.State
            elif ctrl.supportsService("com.sun.star.awt.UnoControlEdit"):
                settings[name] = ctrl.Text
        self._config_save(settings)

    def _load_data(self, dialog, event_name):
        assert dialog.getModel().Name == DIALOG_ID
        for control in dialog.Controls:
            if not control.supportsService("com.sun.star.awt.UnoControlEdit"):
                model = control.Model
                model.Label = _(model.Label)

        if event_name == 'initialize':
            settings = self._config_reader()

            for name in self.cfg_names:
                ctrl = dialog.getControl(name)
                if ctrl.supportsService("com.sun.star.awt.UnoControlCheckBox"):
                    ctrl.setState(settings[name])
                elif ctrl.supportsService("com.sun.star.awt.UnoControlEdit"):
                    ctrl.setText(settings[name])

    def _config_reader(self):
        settings = {}
        reader = getConfigurationAccess(self.cfg_nodes)
        values = reader.getPropertyValues(self.cfg_names)
        for name, value in zip(self.cfg_names, values):
            if not value and reader.Defaults.hasPropertyByName(name):
                value = reader.Defaults.getPropertyValue(name)
            settings[name] = value
        return settings

    def _config_save(self, settings):
        writer = getConfigurationAccess(self.cfg_nodes, True)
        for name, value in settings.items():
            if name == 'test_mode':
                value = bool(value)
            writer.setPropertyValue(name, value)
        writer.commitChanges()

    def getSupportedMethodNames(self):
        return (self.METHOD_NAME,)

    def getImplementationName(self):
        return IMPLEMENTATION_NAME

    def supportsService(self, name):
        return name == SERVICE_NAME

    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)
