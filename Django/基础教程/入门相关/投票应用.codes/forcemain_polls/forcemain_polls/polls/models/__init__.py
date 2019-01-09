#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from functools import partial
from forcemain_polls.utils.module_loading import autodiscovery_modules


modules = autodiscovery_modules(__name__, __file__)


# inject globals
g_data = {}
map(lambda m: g_data.update(m.__dict__), modules)
globals().update(g_data)

autodiscovery = partial(autodiscovery_modules,__name__, __file__)
