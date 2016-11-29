#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''dhead.py'''

from code.packer import *

class DHead(Packer):
	"""docstring for Soiler"""
	def __init__(self,mod):
		self.replace =dict()
		self.replace['18_13'] = '10_11'
		self.replace['19_14'] = '06_10'
		self.replace['20_15'] = '11_09'
		self.replace['21_16'] = '01_08'
		self.replace['22_17'] = '12_07'
		self.replace['23_18'] = '07_06'
		self.replace['24_19'] = '13_05'
		self.replace['25_20'] = '03_04'
		self.replace['26_21'] = '14_03'
		self.replace['27_22'] = '08_02'
		self.replace['28_23'] = '15_01'
		self.replace['29_24'] = '02_00'
		self.replace['30_25'] = '16_31'
		self.replace['31_26'] = '09_30'
		self.replace['32_27'] = '17_29'
		self.subnum = -5
		self.subdirs = ['01_08', '02_00', '03_04','04_12', '05_28', '06_10','07_06', '08_02', '09_30','10_11',
						'11_09','12_07','13_05','14_03','15_01','16_31','17_29','18_13','19_14','20_15',
						'21_16','22_17','23_18','24_19','25_20','26_21','27_22','28_23','29_24','30_25',
						'31_26','32_27']
		self.fstatus = {'1_idle','2_move','3_attack_1','4_attack_2',
						'5_attack_3','6_die_1','7_die_2','8_die_3'}
		self.dealPng(mod)
		Packer.__init__(self, 'towers_head',mod)

	def getModname(self):
		tmp=dict()
		tmp['dota1'] = 'dota_1'
		tmp['dota2'] = 'dota_2'
		tmp['towers_head'] = 'dota_1'
		if self.modname in tmp.keys():
			self.modname = tmp[self.modname]

	def dealPng(self, src):
		realsudirs = scanDir(src)
		for subdir in realsudirs:
			empty = self.getEmptyStatus(subdir)

			ipath = genPath(subdir, '1_idle')
			mpath = genPath(subdir, '2_move')
			apath = genPath(subdir, '3_attack_1')
			a31 = '3_attack_1' in empty
			
			for path in empty:
				dpath = genPath(subdir, '6_die_1')
				dfirstpng = scanFile(dpath)[0]

				#different from dbody
				if path == '7_die_2':
					copyFile(dfirstpng, dfirstpng.replace('6_die_1', '7_die_2'))
				elif path == '8_die_3':
					copyFile(dfirstpng, dfirstpng.replace('6_die_1', '8_die_3'))
				#end 

				elif not a31:
					afirstpng = scanFile(apath)[0]
					dest = afirstpng.replace('3_attack_1',path)
					copyFile(afirstpng, dest)

			os.rename(ipath, ipath.replace('1_idle', '2_idle'))
			os.rename(mpath, mpath.replace('2_move', '3_move'))
			if not a31:
				os.rename(apath, apath.replace('3_attack_1','1_attack_1'))
