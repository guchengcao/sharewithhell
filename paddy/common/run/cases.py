#coding=utf-8

from __future__ import print_function
import importlib
from . import results
from os import listdir

import logging
LOG_DEBUG = lambda m: print('{0}'.format(m)) if __debug__ else logging.debug('{0}'.format(m))
LOG_ERROR = lambda m: print('{0}'.format(m)) if __debug__ else logging.error('{0}'.format(m))
LOG_FATAL = lambda m: print('{0}'.format(m)) if __debug__ else logging.critical('{0}'.format(m))

def _c_load_TC_config(cf):
	try:
		conf = cf.get_TCs_config()
	except AttributeError as e:
		conf = {}

	return conf

def _c_record_result(ret, msg, info, tc_info, tc_conf):
	results.result(ret, msg.encode('utf-8'), info.encode('utf-8'), tc_info, tc_conf)

def _c_run_TC(cf):
	tc_conf = _c_load_TC_config(cf)
	tc_filename = cf.__name__
	for TC in dir(cf):
		if not TC.startswith('TC_'):
			continue

		func = getattr(cf, TC)
		if not callable(func):
			continue

		LOG_DEBUG('+++++++++_run_TC: {0} in {1}'.format(TC, tc_filename))
		try:
			ret, msg, info = func()
			#LOG_DEBUG('cases: _c_run_TC: test')
			#ret, msg, info = 1025, 'yes', 'ok'
		except UnicodeEncodeError as e:
			msg = 'run error: {0}'.format(e.__class__.__name__)
			info = '{0}'.format(e)
			LOG_DEBUG('_run_TC: {0}: {1}'.format(msg, info))
			continue
		except Exception as e:
			ret = -1
			msg = 'run error: {0}'.format(e.__class__.__name__)
			info = '{0}'.format(e)
			LOG_DEBUG('_run_TC: {0}: {1}'.format(msg, info))

		LOG_DEBUG('+++++++++_run_TC Done: ret= {0}, msg= {1}'.format(ret, msg))
		
		tc_info = {
			'TC_File': tc_filename,
			'TC_Name': TC
			}
		_c_record_result(ret, msg, info, tc_info, tc_conf)
		

def _c_load_TC(casepath, casefile):
	cf_name = casefile.rsplit('.', 1)[0]
	obj_cf = importlib.import_module('{0}.{1}'.format(casepath, cf_name))
	_c_run_TC(obj_cf)

def _c_load_TCs(case_conf):
	cp = case_conf.get('casepath')
	prefix = case_conf.get('prefix')
	for case in listdir(cp):
		if case.startswith(prefix) and case.endswith(('.PY', '.py')):
			LOG_DEBUG('==========load_TCs: find case_file: {0}'.format(case))
			_c_load_TC(cp, case)

def start(case_conf):
	while 1:
		try:
			_c_load_TCs(case_conf)
		except KeyboardInterrupt:
			LOG_DEBUG('STOP BY ctrl+c')
			break                    
		except Exception as e:
			LOG_DEBUG('run load_TCs Error:{0}: {1}'.format(e.__class__.__name__, e))
		else:
			LOG_DEBUG('--############## load_TCs Done #################--')
	# end for while 1

