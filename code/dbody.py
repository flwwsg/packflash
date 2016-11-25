#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''dbody.py'''

from code.packer import Packer
import code.packHelper as helper
from os import rename
from os.path import exists

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
		self.subdirs = ['01_04', '02_00', '03_02','04_06', '05_14', '06_05','07_03', '08_01', '09_15','10_07',
						'11_08','12_09','13_10','14_11','15_12','16_13']
		self.dealPng(mod)
		Packer.__init__(self,'towers_body', mod)
		self.getModname()


	def getModname(self):
		tmp=dict()
		tmp['dota1'] = 'dota_1'
		tmp['dota2'] = 'dota_2'
		tmp['towers_body'] = 'dota_1'

		if self.modname in tmp.keys():
			self.modname = tmp[self.modname]

	def dealPng(self, dirsrc):
				
		dirs = helper.scanDir(dirsrc)
		for tmpdir in dirs:
			idle = tmpdir+'/'+'1_idle'
			move = tmpdir+'/'+'2_move'
			a31 = tmpdir+'/'+'3_attack_1'
			for oldname, newname in zip([idle, move, a31],['2_idle','3_move','1_attack_1']):
				if exists(oldname):
					rename(oldname, tmpdir+'/'+newname)

		newemptys = self.getEmpty(dirsrc)
		
		for item in newemptys:
			bn = helper.baseName(item)
			if bn == '7_die_2' or bn =='8_die_3':
				src = item.replace(bn, '6_die_1')
				find = self.chkEmpty(src, newemptys)
				if not find:
					helper.copyFiles(src, item, recur=False)
				continue
			if bn =='1_attack_1':
				continue
			a11 = item.replace(bn, '1_attack_1')
			a11firstpng = helper.scanFile(a11)[0]
			helper.copyFile(a11firstpng, a11firstpng.replace('1_attack_1', bn))

		# exit()

