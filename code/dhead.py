#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''dhead.py'''

from code.packer import Packer
import code.packHelper as helper
from os import rename
from os.path import exists

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
		self.dealPng(mod)
		Packer.__init__(self, 'towers_head',mod)
		self.getModname()

	def getModname(self):
		tmp=dict()
		tmp['dota1'] = 'dota_1'
		tmp['dota2'] = 'dota_2'
		tmp['towers_head'] = 'dota_1'
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
					src = helper.scanFile(src)[0]
					helper.copyFile(src, src.replace('6_die_1', bn))
				continue
			if bn =='1_attack_1':
				continue
			a11 = item.replace(bn, '1_attack_1')
			a11firstpng = helper.scanFile(a11)[0]
			helper.copyFile(a11firstpng, a11firstpng.replace('1_attack_1', bn))