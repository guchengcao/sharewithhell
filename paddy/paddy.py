#coding=utf-8

__version__ = '1.0.2'
__author__  = 'Kangjoe'
__create_time__ = '20160805'
__modify_time__ = '20160921'

'''
frame for automation tester
'''

from os.path import dirname
from os import chdir

import sys
workpath = dirname(sys.argv[0])
chdir(workpath if workpath else '.')

import common.main as paddy
paddy.run()
