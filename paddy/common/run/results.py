#coding: utf-8

from __future__ import print_function
from ..notice import Email
from ..notice import Jira

import logging
LOG_DEBUG = lambda m: print('{0}'.format(m)) if __debug__ else logging.debug('{0}'.format(m))
LOG_ERROR = lambda m: print('{0}'.format(m)) if __debug__ else logging.error('{0}'.format(m))
LOG_FATAL = lambda m: print('{0}'.format(m)) if __debug__ else logging.critical('{0}'.format(m))

def _r_email(ret, msg, info, tc_info, mail_conf):
	if not mail_conf:
		return
	
	handle = Email.send_email
	
	etitle = u'自动化测试执行用例失败(From paddy)'.encode('utf-8')
	econtent = '''
	TC-Name : {0} in {1}
	Err-Code: {2}
	Err-Msg : {3}
	Err-Info: {4}
	'''.format(tc_info.get('TC_Name'), tc_info.get('TC_File'), ret, msg, info)
	
	smtp_srv = mail_conf.get('smtp')
	fromaddr = mail_conf.get('mailfrom')
	toaddrs = mail_conf.get('mailto')
	loginpwd = mail_conf.get('loginpwd')
	
	resp = handle(etitle, econtent, smtp_srv, fromaddr, toaddrs, loginpwd)
	LOG_DEBUG('_r_email: {0}'.format(resp))

def _r_jira(ret, msg, info, tc_info, jira_conf):
	handle = Jira.post_bug
		
	jira_host = jira_conf.get('jira_host', 'http://10.10.63.253:9080')
	jira_user = jira_conf.get('jira_login', 'zhaoganjie:zhaoganjie')
	assignee  = jira_conf.get('assignee', 'zhaoganjie')
	project_key = jira_conf.get('project_key', 'YC')
	issue_type  = jira_conf.get('bug_type', 'Bug')
	
	bug_info = {
		'fields': {
			'project': {'key': project_key},
			'summary': '[{0} in {1}]{2};errcode={3}'.format(tc_info.get('TC_Name'), tc_info.get('TC_File'), msg, ret),
			'description': info,
			'assignee': {'name': assignee},
			'issuetype': {'name': issue_type}
		}
	}
	
	resp = handle(jira_host, jira_user, bug_info)
	LOG_DEBUG('_r_jira: {0}'.format(resp))

def _r_record_result(ret, msg, info, tc_info, tc_conf):
	pass

def _r_notice_result(ret, msg, info, tc_info, tc_conf):
	if ret == 0:
		return

	rule = tc_conf.get('rule', [])
	if len(rule) == 0: # no rule
		_r_email(ret, msg, info, tc_conf)
	else:
		for key, notify in rule:
			if eval(key):
				if 'email' in notify.split(','):
					_r_email(ret, msg, info, tc_info, tc_conf.get('email', None))
				if 'jira' in notify.split(','):
					_r_jira(ret, msg, info, tc_info, tc_conf.get('jira', None))
			else: # key == false
				_r_email(ret, msg, info, tc_info, tc_conf.get('email', None))
	
def result(ret, msg, info, tc_info, tc_conf):
	_r_record_result(ret, msg, info, tc_info, tc_conf)
	_r_notice_result(ret, msg, info, tc_info, tc_conf)
			
