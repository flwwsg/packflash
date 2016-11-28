#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''dbody.py'''

from code.packer import *

class DBody(Packer):
	"""docstring for Body"""
	def __init__(self, mod):
		self.replace =dict()
		self.replace['10_07'] = '06_05'
		self.replace['11_08'] = '01_04'
		self.replace['12_09'] = '07_03'
		self.replace['13_10'] = '03_02'
		self.replace['14_11'] = '08_01'
		self.replace['15_12'] = '02_00'
		self.replace['16_13'] = '09_15'

		self.subnum = -5
		self.subdirs = ['01_04', '02_00', '03_02','04_06', '05_14', '06_05','07_03', '08_01', '09_15']
		self.fstatus = {'1_idle','2_move','3_attack_1','4_attack_2',
						'5_attack_3','6_die_1','7_die_2','8_die_3'}
		self.dealPng(mod)
		Packer.__init__(self,'towers_body', mod)

	def getModname(self):
		tmp=dict()
		tmp['dota1'] = 'dota_1'
		tmp['dota2'] = 'dota_2'
		tmp['towers_body'] = 'dota_1'

		if self.modname in tmp.keys():
			self.modname = tmp[self.modname]

	def dealPng(self, src):
		realsudirs = scanDir(src)
		for subdir in realsudirs:
			empty = self.getEmptyStatus(subdir)

			ipath = genPath(subdir, '1_idle')
			mpath = genPath(subdir, '2_move')
			apath = genPath(subdir, '3_attack_1')
			a31 = '3_attack_1' in empty:
			
			for path in empty:
				dpath = genPath(subdir, '6_die_1')
				if path == '7_die_2':
					copyFiles(dpath, dpath.replace('6_die_1', '7_die_2'))
				elif path == '8_die_3':
					copyFiles(dpath, dpath.replace('6_die_1', '8_die_3'))
				elif not a31:
					afirstpng = scanFile(apath)[0]
					dest = afirstpng.replace('3_attack_1',path)
					copyFile(afirstpng, dest)

			os.rename(ipath, ipath.replace('1_idle', '2_idle'))
			os.rename(mpath, mpath.replace('2_move', '3_move'))
			if not a31:
				os.rename(apath, apath.replace('3_attack_1','1_attack_1'))


