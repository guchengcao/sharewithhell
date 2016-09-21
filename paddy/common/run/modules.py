#coding=utf-8

from __future__ import print_function
import importlib
from os import listdir
from threading import Thread as start_thread

g_mods = []

import logging
LOG_DEBUG = lambda m: print('{0}'.format(m)) if __debug__ else logging.debug('{0}'.format(m))
LOG_ERROR = lambda m: print('{0}'.format(m)) if __debug__ else logging.error('{0}'.format(m))
LOG_FATAL = lambda m: print('{0}'.format(m)) if __debug__ else logging.critical('{0}'.format(m))

def _m_start_module_imp(obj_module):
	try:
		obj_module.run()
	except Exception as e:
		LOG_DEBUG('__start_module__:{0}: {1}: {2}'.format(obj_module.__name__, e.__class__.__name__, e))


def _m_load_module(mods_path, mod):
	mod_name = mod.rsplit('.', 1)[0]
	obj_mod = importlib.import_module('{0}.{1}'.format(mods_path, mod_name))
	t = start_thread(target=_m_start_module_imp, args=(obj_mod, ))
	t.start()
	return obj_mod

def start(mod_conf):
	global g_mods
	mp = mod_conf.get('modulepath')
	prefix = mod_conf.get('prefix')
	
	for mod in listdir(mp):
		if mod.startswith(prefix) and mod.endswith(('.PY', '.py')):
			LOG_DEBUG('load_modules: find module file: {0}'.format(mod))
			try:
				om = _m_load_module(mp, mod)
				g_mods.append(om)
			except Exception as e:
				LOG_DEBUG('load_module:{0}: {1}: {2}'.format(mod, e.__class__.__name__, e))

def stop():
	for om in g_mods:
		try:
			om.stop()
		except Exception as e:
			LOG_DEBUG('m_stop:{0}: {1}: {2}'.format(om.__name__, e.__class__.__name__, e))
			
