#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''building.py'''

from code.packHelper import *
from code.packer import *

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

	def runAll(self, jsfl, ttdir, fdir, flock):
		self.renameSubdir(self.fpath)
		out = ttdir+'/'+baseName(self.fpath)
		self.ttpack(self.fpath,out)       #xmlpaths = dict(1_2=xx.xml)
		cutout =out+ '_cut'

		#cutting small picture saved at tmp/texture/xxx_cut from picture processed by texture on tmp/texture/xxx
		self.ttcutimg(out)  

		#执行扫描并生成config.xml  
		pdata = PackData(cutout)
		pdata.countPics()
		pdata.getitems(out, self.replace)

		#执行扫描并生成xml
		cmds = []
		for subdir in pdata.subdir:

			fname = self.modname+'_'+subdir
			fullname = self.fullname+'_'+subdir     #for multiple threading 
			pdata.genjsfl(fullname,jsfl)
			pdata.genroot(fname)
			pdata.witem()
			pdata.wbody(pdata, subdir, self.replace)
			fpath = genPath(jsfl,fullname+'.xml')
			pdata.savexml(fpath)
			
			cmds.append(fpath[:-3]+'jsfl')

		with flock:
			for cmd in cmds:
				os.system(cmd)
				location = self.mv2finalSource(fdir, jsfl, fname)