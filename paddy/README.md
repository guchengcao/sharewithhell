paddy: 寓义稻田，你可以在上面种植你想要的农作物。

在本框架中，取义为：模块插件化，用例插件化。
模块插件化：根据既定规则，你可以自定义任意模块，框架在启动时，会自动载入模块并调用run函数
用例插件化：根据既定规则，你可以自定义任意用例，框架在运行时，会动态载入用例并执行，且能根据配置项将结果通知到相关人员。

模块规则：
1、每个模块中必须有名为"run"的函数, 最好同时有"stop"函数，Paddy会加载模块，并自动调用run函数，结束时会调用stop函数
2、在Modules目录下，新建一个或多个py脚本，且命名必须满足： MOD_.*.py正则，即必须以MOD_开头; paddy.ini中可配置该前缀
3、模块文件一般用于管理及监控用例执行环境。
4、run函数可以是阻塞式的，直到stop函数被调用再结束退出。

用例规则：
1、在Cases目录下，新建一个或多个py脚本，且命名必须满足： TCs_.*.py正则，即必须以‘TCs_开头’; 前缀可配
2、每条用例以一个函数来承载，且函数名必须满足：TC_.*正则，即必须以‘TC_’开头; 注: 前缀不可配
3、用例定义：不接受参数、不长时间无返回
4、用例返回值：return (ret, msg, info); ret为错误码，为0时表示执行成功；msg为短信息，一般用于简述BUG所在；info为具体信息，用于邮件中的正文，或者jira中的BUG描述
5、用例配置函数，必须命名为: get_TCs_config, 如果找不到这个名字的函数，则使用默认配置项。以下为该函数试例：
def get_TCs_config():
	TCs_Conf = {
		'rule': [ # 通知规则的定义,默认的通知方式: email
			  # 自定义通知规则, 目前只支持用例的返回错误码
				('ret<8', 'email'),	# 错误码小于8时，使用邮件通知
				('ret>=8', 'jira'),	# 错误码大于8时，提交BUG到Jira
				('ret>1024', 'email,jira'),	# 错误码大于1024时，邮件通知，同时提交BUG
			],
		
		'email': { # email项为可选
			'smtp': 'mail.163.com', #发送邮件使用的smtp服务器
			'mailfrom': 'jie800@163.com', #用于发送邮件的账号
			'loginpwd': 'password for email',
			'mailto': 'jie800@163.com, someoneelse@163.com',  # 如果配置了email项，则必须要配置 mailto项
			'subject': u'自动化测试执行用例失败(From paddy)', # 该参数为可选
		},

		'jira': {
			'jira_host': 'http://10.10.63.253:9080',
			'jira_login': 'zhaomoumou:zhaomoumou',  # 登陆jira的用户名及密码，使用英文冒号分隔
			'bug_prefix': '[Auto-Bug-Paddy]', # 提交的Bug的标题的前缀，可选。 
			'assignee': 'some_developer', # BUG指派
			'project_key': 'YC', # 在jira中创建project时，指定的key
			'bug_type': 'Bug', #在jira中创建bug时，选择bug类型
		}
	}

	return TCs_Conf

框架运行方法:
python -O paddy.py
