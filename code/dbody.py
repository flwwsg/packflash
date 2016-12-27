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
		Packer.__init__(self,'towers_body', mod, 0)
		self.getModname()

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
			apath = genPath(subdir, '3_attack_1')
			ipath = genPath(subdir, '1_idle')
			a31 = '3_attack_1' in empty
			idle = '1_idle' in empty
			dpath = genPath(subdir, '6_die_1')

			for path in empty:
				if path == '7_die_2':
					copyFiles(dpath, dpath.replace('6_die_1', '7_die_2'))
				elif path == '8_die_3':
					copyFiles(dpath, dpath.replace('6_die_1', '8_die_3'))
				elif not a31:
					afirstpng = scanFile(apath)[0]
					path = self.chkdir(path)
					dest = afirstpng.replace('3_attack_1',path)
					copyFile(afirstpng, dest)	
				elif not idle:
					ilastpng = scanFile(ipath)[-1]
					path = self.chkdir(path)
					dest = ilastpng.replace('1_idle',path)
					copyFile(ilastpng, dest)					

			if not a31:
				os.rename(apath, apath.replace('3_attack_1','1_attack_1'))
			if not idle:
				os.rename(ipath, ipath.replace('1_idle','2_idle'))

	def chkdir(self, oldir):
		tmp =dict()
		tmp['1_idle'] = '2_idle'
		tmp['2_move'] = '3_move'
		tmp['3_attack_1'] = '1_attack_1'
		if oldir in tmp.keys():
			return tmp[oldir]
		else:
			return oldir