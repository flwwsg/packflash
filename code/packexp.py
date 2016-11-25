#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime
import code.packHelper as helper
import os

class PackExp(Exception):
	def __init__(self, logs,fname='errors.txt'):
		self.logs = logs
		self.getPath()
		self.logfile=os.path.join(self.logpath,fname)

	def wlog(self):
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		with open(self.logfile,'a',encoding='utf-8') as fs:
			fs.write('\n'+self.logs+'\t'+now)

	def getPath(self):
		root = os.getcwd()
		self.logpath = os.path.join(root, 'logs')

	def mail(self, receiver, subject, fname=None, mbody=None ):
		helper.smail(receiver=receiver, subject=subject, fname=fname, mbody=mbody)

class LastOpNotClean(PackExp):
	def __init__(self, logs=''):
		logs = '上次运行时程序意外中止，请查看tmp目录'+logs
		PackExp.__init__(self, logs, 'errors.txt')

	def wlog(self):
		PackExp.wlog(self)
		receiver=helper.MYRECEIVER
		subject=self.logs
		mbody = self.logs
		self.mail(receiver=receiver, subject=subject, mbody=mbody)

class SVNotFound(PackExp):
	def __init__(self,logs):
		PackExp.__init__(self, logs, 'errors.txt')

	def wlog(self):
		PackExp.wlog(self)