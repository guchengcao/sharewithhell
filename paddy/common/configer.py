#coding:utf-8

import ConfigParser

MAIN_GOGOGO =  __name__ == '__main__'
def gpc_debug(msg):
	if MAIN_GOGOGO:
		print('{0}'.format(msg))
		
class GetPaddyConfig:
	def __init__(self, fp, filepath=None):
		self._cp = ConfigParser.ConfigParser()
		if fp:
			self._cp.readfp(fp)
		else:
			if filepath:
				with open(filepath) as fp:
					self._cp.readfp(fp)
			else:
				self._cp = None	

		self._get_config()

	def get_module_config(self):
		return self._module

	def get_case_config(self):
		return self._case

	def get_plugin_config(self):
		return self._plugin

	def get_email_config(self):
		return self._email

	def get_jira_config(self):
		return self._jira
		
	def _get_config(self):
		self._module = self._get_module_config()
		self._case = self._get_case_config()
		self._plugin = self._get_plugin_config()
		self._email = self._get_email_config()
		self._jira = self._get_jira_config()
		
		gpc_debug('gpc._get_config: paddy= {0},\nemail= {1},\njira= {2}'.format(self._case, self._email, self._jira))

	def _get_module_config(self):
		cp = self._cp
		section = 'Modules'
		conf = {
			'prefix': 'Mod',
			'modulepath': 'Modules'
		}

		for key in conf:
			if cp.has_option(section, key):
				conf[key] = cp.get(section, key)
				
		return conf

	def _get_case_config(self):
		cp = self._cp
		section = 'Cases'
		conf = {
			'prefix': 'TCs',
			'casepath': 'Cases'
		}

		for key in conf:
			if cp.has_option(section, key):
				conf[key] = cp.get(section, key)
				
		return conf

	def _get_plugin_config(self):
		cp = self._cp
		section = 'Plugins'
		conf = {
			'suffix': 'sh, py',
			'plugpath': 'plugins'
		}

		for key in conf:
			if cp.has_option(section, key):
				conf[key] = cp.get(section, key)
				
		return conf

	def _get_email_config(self):
		cp = self._cp
		section = 'Email'
		conf = {
			'sendfrom': 'zhaoganjie@xunlei.com',
			'sendto': ['zhaoganjie@xunlei.com', 'jie800@163.com'],
			'mailserver': 'mail.xunlei.com',
			'mailpwd': 'yIG6aKSJ',
		}

		for key in conf:
			if cp.has_option(section, key):
				if key == 'sendto':
					value = cp.get(section, key)
					conf[key] = [i.strip() for i in value.split(',')]
				else:
					conf[key] = cp.get(section, key)
				
		return conf

	def _get_jira_config(self):
		cp = self._cp
		section = 'Jira'
		conf = {
			'jiraserver': 'http://10.10.63.253:9080',
			'jirauser': 'zhaoganjie',
			'jirapwd': 'zhaoganjie',
			'bugassign': 'zhaoganjie',
			'bugprefix': '[Auto-Bug-Paddy]',
			'bugtype': 'Bug',
			'projectkey': 'YC',
		}

		for key in conf:
			if cp.has_option(section, key):
				conf[key] = cp.get(section, key)
				
		return conf
				
if MAIN_GOGOGO:
	filepath = '../paddy.ini'
	gpc = GetPaddyConfig(fp=None, filepath=filepath)
	p = gpc.get_paddy_config()
	e = gpc.get_email_config()
	j = gpc.get_jira_config()
	gpc_debug('paddy= {0},\nemail= {1},\njira= {2}'.format(p, e, j))

