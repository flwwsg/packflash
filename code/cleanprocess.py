#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import code.packHelper as helper
import os
from code.packexp import SVNotFound

def cleanprocess(tmpdir, body=''):
	helper.rmDir(tmpdir)
	receiver = helper.MYRECEIVER
	subject = helper.SUCCSUBJECT
	mbody = helper.SUCCBODY % body
	helper.smail(receiver=receiver, subject=subject, mbody=mbody)

def getSvnAddr(fname,mtype, types):
	root = os.getcwd()
	file = root+'/svn.txt'
	with open(file) as f:
		for line in f.readlines():
			for dirs, subdirs, fns in os.walk(line):
				for fn in fns:
					if fn == fname and dirs.find(types) != -1 and dirs.find(mtype) != -1:
						return dirs
	return False

#types = solider ... ,mtype = mobs , units ...
def copy2SVN(src, mtype, types):
	fname = os.path.basename(src)
	find = getSvnAddr(fname, types, mtype)
	if not find:
		msg ='Can not find type of %s named %s in svn address' %(types, fname)
		raise SVNotFound(msg)
	else:
		helper.copyFile(src, find+'/'+fname)