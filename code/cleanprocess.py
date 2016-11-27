#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from code.packHelper import *
from code.packexp import *

class Cleanprocess:
		
	@staticmethod
	def cleanprocess(tmpdir, startime, body=''):
		rmDir(tmpdir)
		if not body:
			return
		raise PackFinish(startime, body)

	@staticmethod
	def getSvnAddr(fname,types,mtype):
		root = os.getcwd()
		file = root+'/svn.txt'
		with open(file) as f:
			for line in f.readlines():
				for dirs, subdirs, fns in os.walk(line):
					for fn in fns:
						if fn == fname and dirs.find(types) != -1 and dirs.find(mtype) != -1:
							return dirs, file
		return False,file

	#types = solider ... ,mtype = mobs , units ...
	@staticmethod
	def copy2SVN(src, types,mtype):
		fname = os.path.basename(src)
		find, svnfile = Cleanprocess.getSvnAddr(fname, types, mtype)
		if not find:
			raise SVNotFound(svnfile, types, mtype, fname)
		else:
			copyFile(src, find+'/'+fname)