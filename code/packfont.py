#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from code.packer import *
from code.fontdata import FontData

class PackFont(Packer):
	def __init__(self, file):
		fname, ext = os.path.splitext(file)
		self.file = file
		self.modname = baseName(fname)
		self.modtype = 'font'
		self.type = self.modname
		self.fullname = '-'.join([self.modname, self.modtype, self.type])

	def runAll(self, jsfl, ttdir, fdir, flock):
		#执行扫描并生成{self.fullname}xml  
		pdata = FontData()
		pdata.genjsfl(self.fullname,jsfl)
		pdata.genroot(self.modname)
		pdata.witem()

		for line in open(self.file,encoding='utf-8'):
			pdata.wbody(line)
		fname = genPath(jsfl,self.fullname+'.xml')
		pdata.savexml(fname)
		
		with flock:
			os.system(fname[:-3]+'jsfl')
			location = self.mv2finalSource(fdir, jsfl)

		