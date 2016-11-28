#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''soilder.py'''

from code.packer import *

class Soldier(Packer):
	
	def __init__(self,mod):
		self.replace =dict()
		self.replace['6_6'] = '2_0'
		self.replace['7_5'] = '3_1'
		self.replace['8_4'] = '1_2'
		self.subnum = -3
		self.subdirs = ['1_2','2_0','3_1','4_7','5_3']  #'6_6','7_5','8_4']
		self.fstatus = {'1_idle', '2_move', '3_attack_1', '4_attack_2', 
						'5_attack_3', '6_die_1','7_die_2', '8_die_3'}
		self.dealPng(mod)
		Packer.__init__(self, 'soldiers',mod)

#subdir = 1_2, 2_0 xx
	def dealPng(self, src):
		realsubdirs = scanDir(src)
		for subdir in realsubdirs:
			empty = self.getEmptyStatus(subdir)
			if '2_move' in empty:
				for path in empty:
					diesrc = genPath(subdir,'6_die_1')
					if 'die' in path:
						diedest = genPath(subdir,path)
						copyFiles(diesrc, diedest)
			else:
				mpath = genPath(subdir, '2_move')
				movelastpng = scanFiles(mpath)[-1]
				diesrc = genPath(subdir,'6_die_1')
				for path in empty:
					if 'attack' in path:
						dest = movelastpng.replace('2_move', path)
						copyFile(movelastpng, dest)
					elif 'die' in path:
						diedest = genPath(subdir,path)
						copyFiles(diesrc, diedest)