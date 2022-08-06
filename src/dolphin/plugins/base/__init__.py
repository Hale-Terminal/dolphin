from __future__ import absolute_import, print_function

from dolphin.plugins.base.v1 import *
from dolphin.plugins.base.manager import PluginManager

plugins = PluginManager()
register = plugins.register
unregister = plugins.unregister
