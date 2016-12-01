#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from code.packHelper import *
from code.packexp import *

class Cleanprocess:
	def __init__(self):
		self.getpath()
		
	@classmethod
	def getpath(self):
		root = os.getcwd()
		self.tpath = os.path.join(root, 'tmp')
		self.svnfile = os.path.join(root,'svn.txt')

	@classmethod
	def cleanprocess(self,startime, body=''):
		if not DEBUG and PackExp.numIns == 0:
			rmDir(self.tpath)
		raise PackFinish(startime, body)

	@classmethod
	def getSvnAddr(self, fname,types,mtype):
		with open(self.svnfile) as f:
			for line in f.readlines():
				for dirs, subdirs, fns in os.walk(line):
					for fn in fns:
						if fn == fname and dirs.find(types) != -1 and dirs.find(mtype) != -1:
							return dirs
		return False

	#types = solider ... ,mtype = mobs , units ...
	@classmethod
	def copy2SVN(self, src, types,mtype,fullname):
		fname = os.path.basename(src)
		find = self.getSvnAddr(fname, types, mtype)
		if not find:
			raise SVNotFound(self.svnfile, types, mtype, fname, fullname)
		else:
			copyFile(src, find+'/'+fname)