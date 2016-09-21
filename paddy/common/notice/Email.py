#coding:utf-8

import smtplib

def _login_email(smtp, username, userpwd):
	try:
		conn = smtplib.SMTP(smtp)
		conn.login(username, userpwd)
	except Exception as e:
		#print '_login_email:', e.__class__.__name__, str(e)
		conn = None

	return conn

def _send_mail(smtp_conn, fromaddr, toaddrs, subject, content):
	try:
		msg = ("Subject: {0}\r\nFrom: {1}\r\nTo: {2}\r\n\r\n{3}".format(subject, fromaddr, toaddrs, content))
		# print msg
		toaddr_l = [m.strip() for m in toaddrs.split(',')]
		ret = smtp_conn.sendmail(fromaddr, toaddr_l, msg)
		return ret
	except Exception as e:
		msg = '_send_mail: {0}: {1}'.format(e.__class__.__name__, e)
		return msg

def send_email(etitle, econtent, smtp_srv, fromaddr, toaddrs, loginpwd):
	print 'send_email', etitle, econtent, smtp_srv
	if toaddrs is None:
		return 'toaddrs is None'

	smtp_conn = _login_email(smtp_srv, fromaddr, loginpwd)
	if smtp_conn:
		return _send_mail(smtp_conn, fromaddr, toaddrs, etitle, econtent)
	else:
		return 'login smtp failed'
	
