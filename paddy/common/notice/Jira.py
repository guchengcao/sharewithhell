#coding:utf-8
import urllib2
import json
from base64 import b64encode as BasicEnc

def _post_bug(jira_host, jira_user, bug_info):
	full_url = '{0}/rest/api/2/issue/'.format(jira_host)
	enc_user = BasicEnc(jira_user)

	post_header = {
		'Content-Type': 'application/json',
		'Authorization': 'Basic {0}'.format(enc_user)
	}

	post_data = json.dumps(bug_info)
	try:
		req = urllib2.Request(full_url, data=post_data, headers=post_header)
		resp = urllib2.urlopen(req).read()
		return resp
	except Exception as e:
		msg = 'post_bug: {0}: {1}'.format(e.__class__.__name__, e)
		return msg

def post_bug(jira_srv, user, bug_info):
	return _post_bug(jira_srv, user, bug_info)
	


