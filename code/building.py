#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''building.py'''

from code.packer import Packer
from code.packdata import PackData
import code.packHelper as helper
import os
from code.cleanprocess import cleanprocess

class Building(Packer):
	"""docstring for Soiler"""
	def __init__(self, mod):
		self.subnum = -3 #1_1, 1_2 xx
		self.subdirs = ['1_1','1_2','1_3','1_4','1_5']
		self.replace =dict()
		self.types = ['citizen', 'construction','custom','factories','offers',
						'office', 'storages','structural', 'upgrade']
		Packer.__init__(self, 'buildings', mod)
		

	def renameSubdir(self, src):
		print('-'*80,'building.renameSubdir to be implemented\n','-'*80, sep='')

	def runAll(self, jsfl, ttdir, fdir):
		self.renameSubdir(self.fpath)
		out = ttdir+'/'+helper.baseName(self.fpath)
		self.ttpack(self.fpath,out)       #xmlpaths = dict(1_2=xx.xml)
		cutout =out+ '_cut'

		#cutting small picture saved at tmp/texture/xxx_cut from picture processed by texture on tmp/texture/xxx
		self.ttcutimg(out)  

		#执行扫描并生成config.xml  
		pdata = PackData(cutout)
		pngnums =PackData.countPics(cutout,pdata.subdir,pdata.status)
		pngxy = PackData.getitems(out,pdata.subdir,self.replace)

		#执行扫描并生成xml
		subdirs = pdata.subdir[:]
		subdirs.extend(self.replace)
		for subdir in subdirs:
			fname = self.modname+'_'+subdir
			self.runOnce(pdata, pngnums, pngxy, subdir, fname, jsfl, cutout)
			location = self.mv2finalSource(fdir, jsfl, fname)