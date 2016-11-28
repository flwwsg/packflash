#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''bsoldier.py'''

from code.packer import *
# from code.soldier import Soldier
from code.bspdata import BSPdata

class BSoldier(Packer):
	
	def __init__(self,mod):
		self.replace =dict()
		self.replace['2_0'] = '1_2'
		self.replace['3_1'] = '1_2'
		self.replace['4_7'] = '1_2'
		self.replace['5_3'] = '1_2'
		self.replace['6_6'] = '1_2'
		self.replace['7_5'] = '1_2'
		self.replace['8_4'] = '1_2'
		self.subnum = -3
		self.subdirs = ['1_2']
		Packer.__init__(self, 'soldiers',mod)


	def runAll(self, jsfl, ttdir, fdir, flock):
		out = ttdir+'/'+baseName(self.fpath)
		self.ttpack(self.fpath,out)       #xmlpaths = dict(1_2=xx.xml)
		cutout =out+ '_cut'

		#cutting small picture saved at tmp/texture/xxx_cut from picture processed by texture on tmp/texture/xxx
		self.ttcutimg(out)  

		#执行扫描并生成{self.fullname}xml  
		pdata = BSPdata(cutout)
		pdata.countPics()
		pdata.getitems(out, self.replace)
		pdata.genjsfl(self.fullname,jsfl)
		pdata.genroot(self.modname)
		pdata.witem()

		for subdir in pdata.subdir:			
			pdata.wbody(pdata, subdir, self.replace)
		fname = genPath(jsfl,self.fullname+'.xml')
		pdata.savexml(fname)
		
		clean = Cleanprocess()
		with flock:
			os.system(fname[:-3]+'jsfl')
			location = self.mv2finalSource(fdir, jsfl)
			if not os.path.exists(location):
				raise SWFNotFound(location)
			clean.copy2SVN(location, self.type, self.modtype,self.fpath)