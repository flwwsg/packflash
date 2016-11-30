#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime
from code.packHelper import *

class PackExp(Exception):
	def __init__(self, logs,fname='errors.txt'):
		self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.logs = logs
		self.getPath()
		self.logfile=os.path.join(self.logpath,fname)

	def wlog(self):
		with open(self.logfile,'a',encoding='utf-8') as fs:
			fs.write('\n'+self.logs+'\t'+self.now)

	def getPath(self):
		root = os.getcwd()
		self.logpath = os.path.join(root, 'logs')

	def mail(self, subject, fname=None ):
		receiver = MYRECEIVER
		mbody = self.logs+'\n邮件发送于'+self.now
		smail(receiver=receiver, subject=subject, fname=fname, mbody=mbody)

class LastOpNotClean(PackExp):
	def __init__(self, logs=''):
		logs = LASTOPNOTCLEAN +logs
		PackExp.__init__(self, logs, 'errors.txt')

	def wlog(self):
		PackExp.wlog(self)
		subject=self.logs
		self.mail( subject=subject)

class SVNotFound(PackExp):
	def __init__(self,svnfile,types, mtype, fname,fpath, logs=''):
		msg = SVNOTFOUND %(types, mtype, fpath, fname)
		self.fname = svnfile
		PackExp.__init__(self, msg+logs, 'errors.txt')

	def wlog(self):
		PackExp.wlog(self)
		subject = self.logs
		self.logs = self.logs
		self.mail( subject=subject, fname=self.fname)

class PackFinish(PackExp):
	def __init__(self, startime, body='', logs=''):
		self.subject = SUCCSUBJECT
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		logs = SUCCBODY % (body, startime, now) + logs
		PackExp.__init__(self, logs)

	def wlog(self):
		self.mail(subject=self.subject)

class SWFNotFound(PackExp):
	def __init__(self, fpath):
		logs = fpath + 'not exists!!! something wrong.'
		PackExp.__init__(self, logs)		

class JobsDone(PackExp):
	def __init__(self, logs=''):
		logs = 'src目录没有文件需要打包' + logs
		PackExp.__init__(self, logs)
		