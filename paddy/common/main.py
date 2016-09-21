#coding:utf-8

from __future__ import print_function
from . import configer
from .run import modules
from .run import cases
from .run import plugins

import logging
LOG_DEBUG = lambda m: print('{0}'.format(m)) if __debug__ else logging.debug('{0}'.format(m))
LOG_ERROR = lambda m: print('{0}'.format(m)) if __debug__ else logging.error('{0}'.format(m))
LOG_FATAL = lambda m: print('{0}'.format(m)) if __debug__ else logging.critical('{0}'.format(m))

def _get_config():
	with open('paddy.ini') as fp:
		gpc = configer.GetPaddyConfig(fp)	
		m = gpc.get_module_config()	
		c = gpc.get_case_config()	
		p = gpc.get_plugin_config()

		return m, c, p

def _init():
	logging.basicConfig(level=logging.DEBUG,
		format='[%(asctime)s] [%(levelname)s]: %(message)s',
		filename='paddy.log')
	
	LOG_DEBUG('main: ready go!')
	
def _uninit():
	modules.stop()
	LOG_DEBUG('main: bye-bye!')

def _start_modules(p):
	modules.start(p)	

def _start_plugins(p):
	#plugins.start(p)	
	pass

def _load_cases(c):
	cases.start(c)

def run():
	_init()
	m, c, p = _get_config()
	_start_modules(m)
	#_start_plugins(p)
	_load_cases(c)
	_uninit()


