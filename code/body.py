#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''body.py'''

from code.packer import *

class Body(Packer):
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
		Packer.__init__(self,'vehicles_body', mod)


	def dealPng(self, src):
		realsudirs = scanDir(src)
		for subdir in realsudirs:
			empty = self.getEmptyStatus(subdir)
			if '3_attack_1' in empty:
				if '2_move' in empty:
					if not '1_idle' in empty:
						ipath = genPath(subdir, '1_idle')
						idlelastpng = scanFile(ipath)[-1]

						for dest in ['2_move','3_attack_1', '4_attack_2', '5_attack_3']:
							newpath = idlelastpng.replace('1_idle',dest )
							copyFile(idlelastpng, newpath)
					if not '6_die_1' in empty:
						dpath = genPath(subdir, '6_die_1')
						dielastpng = scanFile(dpath)[-1]
						for dest in ['7_die_2', '8_die_3']:
							newpath = dielastpng.replace('6_die_1', dest)
							copyFile(dielastpng, newpath)
				else:
					mpath = genPath(subdir, '2_move')
					movelastpng = scanFile(mpath)[-1]
					for dest in ['3_attack_1', '4_attack_2', '5_attack_3']:
							newpath = movelastpng.replace('2_move',dest )
							copyFile(movelastpng, newpath)

					if '1_idle' in empty:
						newpath = movelastpng.replace('2_move','1_idle')
						copyFile(movelastpng, newpath)

					if not '6_die_1' in empty:
						dpath = genPath(subdir, '6_die_1')
						dielastpng = scanFile(dpath)[-1]
						for dest in ['7_die_2', '8_die_3']:
							newpath = dielastpng.replace('6_die_1', dest)
							copyFile(dielastpng, newpath)
			else:
				apath = genPath(subdir, '3_attack_1')
				a31firstpng = scanFile(apath)[0]
				ipath = genPath(subdir,'1_idle')
				if '1_idle' in empty:
					if '2_move' in empty:
						dest = a31firstpng.replace('3_attack_1','1_idle')
						copyFile(a31firstpng, dest)
					else:
						mpath = genPath(subdir, '2_move')
						mfirstpng = scanFile(mpath)[0]
						dest = mfirstpng.replace('2_move','1_idle')
						copyFile(mfirstpng, dest)

				if '2_move' in empty:
					dest = genPath(subdir, '2_move')
					copyFiles(ipath,dest)
				if '4_attack_2' in empty:
					dest = a31firstpng.replace('3_attack_1', '4_attack_2')
					copyFile(a31firstpng, dest)
				if '5_attack_3' in empty:
					dest = a31firstpng.replace('3_attack_1', '5_attack_3')
					copyFile(a31firstpng, dest)
				if '6_die_1' in empty:
					for die in ['6_die_1', '7_die_2', '8_die_3']:
						dest = a31firstpng.replace('3_attack_1', die)
						copyFile(a31firstpng, dest)
				else:
					dpath = genPath(subdir, '6_die_1')
					dielastpng = scanFile(dpath)[-1]
					for die in ['7_die_2', '8_die_3']:
						dest = dielastpng.replace('6_die_1', die)
						copyFile(dielastpng, dest)