#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''head.py'''

from code.packer import *

class Head(Packer):
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
						'11_09','12_07','13_05','14_03','15_01','16_31','17_29']
		self.fstatus = {'1_idle','2_move','3_attack_1','4_attack_2',
						'5_attack_3','6_die_1','7_die_2','8_die_3'}
		self.dealPng(mod)
		Packer.__init__(self, 'vehicles_head',mod)


	def dealPng(self, src):
		realsudirs = scanDir(src)
		for subdir in realsudirs:
			empty = self.getEmptyStatus(subdir)
			#the same as body
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

			#different from body
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

				#different from body
				if '4_attack_2' in empty:
					dest = genPath(subdir,'4_attack_2')
					copyFile(apath, dest)
				if '5_attack_3' in empty:
					dest = genPath(subdir,'5_attack_3')
					copyFile(apath, dest)

				#the same as body
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