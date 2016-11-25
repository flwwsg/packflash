#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''preprocess.py'''

import code.packHelper as helper
import os 
from code.packexp import *

def preprocess():
	root 		= os.getcwd()
	srcdir 		= os.path.join(root, 'src')
	tpath 		= os.path.join(root, 'tmp')
	tspath 		= os.path.join(tpath, 'tempsource')
	ttpath 		= os.path.join(tpath, 'texture')
	finalpath 	= os.path.join(root, 'finalsource')
	logpath 	= os.path.join(root, 'logs')
	kpjsfl 		= os.path.join(tpath, 'kpjsfl')
	tmp 		= [tspath, ttpath, finalpath,logpath, kpjsfl]
	helper.mkDir(tmp)

	renameCN(srcdir)
	dirs = helper.scanDir(srcdir)

	#scan files
	copy2tmpsrc(dirs, tspath)

	fn = dict(tsrcdir=tspath, ttdir=ttpath,fdir=finalpath, 
			srcdir=srcdir, logdir=logpath, kpjsfl=kpjsfl,tpath=tpath)
	return fn

def copy2tmpsrc(dirs, dest, name=None):
	# print(dirs)
	for path in dirs:
		newpath = chkPath(path)
		if len(newpath) < 5:
			bn = helper.baseName(path)
			mod = formatType(bn)
			if name:
				mod = mod +'#'+ name
			copy2tmpsrc(newpath, dest, mod)
			continue
		src = newpath[0]
		if not src:
			return
		src = helper.dirName(src)
		bn = helper.baseName(path)
		mod = formatType(bn)
		if name:
			mod = mod +'#'+ name
		newdest = helper.genPath(dest, mod)
		
		if os.path.exists(newdest):
			# continue
			raise LastOpNotClean()
		helper.copyFiles(src, newdest)
		reFiles(newdest)

def reFiles(dest):
	dirs = helper.scanDir(dest)
	if len(dirs) < 10:
		return
	else:
		replace =dict()
		for x in range(0,10):
			n = str(x)
			replace[n] = '0'+n
		# print(replace)
		for tdir in dirs:
			bn = os.path.basename(tdir)
			tmp = bn.split('_')
			first = tmp[0]
			second = tmp[1]
			newfirst = replace[first] if first in replace.keys() else first
			newsecond = replace[second] if second in replace.keys() else second

			newname = tdir.replace(bn, newfirst+'_'+newsecond)
			os.rename(tdir, newname)			

def chkPath(path):
	dirs = helper.scanDir(path)
	if len(dirs) > 1:
		return dirs
	else:
		return chkPath(dirs[0])

def formatType(fn):
	head = fn[2:3]
	if head == '-':
		return fn[3:]+'-'+fn[:2]
	else:
		return fn

def renameCN(srcdir):
	types =dict(zf='正方',ff='反方',jz='建筑',tx='特效',ui='gui')
	dirs = helper.scanDir(srcdir)

	for item in dirs:
		bn = helper.baseName(item)

		tailcn = bn[-2:]
		headcn = bn[:2]

		for k,v in types.items():
			if v == tailcn:
				newname = item[:-2]+'-'+k
				os.rename(item, newname)
			elif v == headcn:
				newname = item[2:]+'-'+k
				os.rename(item, newname)


		