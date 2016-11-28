#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''preprocess.py'''

from code.packHelper import *
from code.packexp import *

class Preprocess(object):
	"""rename directory and copy files"""
	def __init__(self):
		self.getpath()

	@classmethod
	def getpath(self):
		root 		= os.getcwd()
		tpath 		= os.path.join(root, 'tmp')
		srcdir 		= os.path.join(root, 'src')
		tspath 		= os.path.join(tpath, 'tempsource')
		ttpath 		= os.path.join(tpath, 'texture')
		finalpath 	= os.path.join(root, 'finalsource')
		logpath 	= os.path.join(root, 'logs')
		kpjsfl 		= os.path.join(tpath, 'kpjsfl')
		tmp 		= [tspath, ttpath, finalpath,logpath, kpjsfl,srcdir]

		mkDir(tmp)
		self.tpath = tpath
		self.tspath = tspath
		self.ttpath = ttpath
		self.finalpath = finalpath
		self.logpath = logpath
		self.kpjsfl = kpjsfl
		self.srcdir = srcdir

	@classmethod
	def preprocess(self):
		self.formatType()
		dirs = emptyDir(self.srcdir)
		rmDir(dirs)
		dirs = scanDir(self.srcdir)
		self.copy2tmpsrc(dirs, self.tspath)

	@classmethod
	def copy2tmpsrc(self,dirs, dest, name=None):
		# print(dirs)
		for path in dirs:
			newpath = self.chkPath(path)
			if len(newpath) < 5:
				mod = baseName(path)
				if name:
					mod = mod +'#'+ name
				self.copy2tmpsrc(newpath, dest, mod)
				continue
			src = self.getsrc(newpath[0])
			mod = baseName(path)
			if name:
				mod = mod +'#'+ name
			newdest = genPath(dest, mod)
			
			if os.path.exists(newdest):
				if DEBUG:
					continue
				else:
					raise LastOpNotClean()
			copyFiles(src, newdest)
			self.reFiles(newdest)

	@classmethod
	def reFiles(self, dest):
		files = scanFile(dest)	
		delFiles(files)
		dirs = scanDir(dest)
		if len(dirs) < 10:
			return
		else:
			replace =dict()
			for x in range(0,10):
				n = str(x)
				replace[n] = '0'+n
			# print(replace)
			for tdir in dirs:
				bn = baseName(tdir)
				tmp = bn.split('_')
				if len(tmp) != 2:
					rmDir(tdir)
					continue
				first = tmp[0]
				second = tmp[1]
				newfirst = replace[first] if first in replace.keys() else first
				newsecond = replace[second] if second in replace.keys() else second

				newname = tdir.replace(bn, newfirst+'_'+newsecond)
				os.rename(tdir, newname)	

	@classmethod
	def chkPath(self, path):
		dirs = scanDir(path)
		if len(dirs) > 1:
			return dirs
		else:
			return self.chkPath(dirs[0])

	@classmethod
	def formatType(self):
		types =dict(zf='正方',ff='反方',jz='建筑',tx='特效',ui='gui')
		dirs = scanDir(self.srcdir)

		for item in dirs:
			find = False
			bn = baseName(item)
			tailcn = bn[-2:]
			headcn = bn[:2]
			for k,v in types.items():
				if v == tailcn:
					newname = bn[:-2]+'-'+k
					find = True
					break
				elif v == headcn:
					newname = bn[2:]+'-'+k
					find = True
					break
			if find:
				os.rename(item, item.replace(bn, newname))
			else:
				bn = baseName(item)
				head = bn[2:3]
				if head == '-':
					newname = bn[3:]+'-'+bn[:2]
					os.rename(item, item.replace(bn, newname))
	
	@classmethod
	def getsrc(self, src):
		keep = ['1_2']
		tmp = src.split(os.sep)
		bn = tmp[-2]
		newsrc = os.sep.join(tmp[:-2])
		src = dirName(src)
		if bn in keep:
			return newsrc
		else:
			return src
