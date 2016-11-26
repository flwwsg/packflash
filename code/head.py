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
						'11_09','12_07','13_05','14_03','15_01','16_31','17_29','18_13','19_14','20_15',
						'21_16','22_17','23_18','24_19','25_20','26_21','27_22','28_23','29_24','30_25',
						'31_26','32_27']
		self.dealPng(mod)
		Packer.__init__(self, 'vehicles_head',mod)


	def dealPng(self, dirsrc):
		newemptys = self.getEmpty(dirsrc)
		exists = nonemptyDir(dirsrc)

		a31exits= list()
		for exist in exists:
			if exist.find('3_attack_1') != -1:
				a31exits.append(exist)
		# print(a31exits)
		# exit()
		# print(newemptys)
		if not newemptys:
			return
		attack31 = list()
		moves = list()
		attacks = list()
		dies = list() 
		idles = list()

		for item in newemptys:
			if item.find('2_move') != -1:
				moves.append(item)
				continue
			if item.find('4_attack_2') != -1 or item.find('5_attack_3') != -1:
				attacks.append(item)
				continue
			if item.find('3_attack_1') != -1:
				attack31.append(item)
				continue
			if item.find('6_die_1') != -1 or item.find('7_die_2') != -1 or item.find('8_die_3') != -1:
				dies.append(item)
				continue
			if item.find('1_idle') != -1:
				idles.append(item)
				continue
		# print(attack31)
		#3_attack_1 is empty:
		for a3 in attack31:        
			#2_move is empty
			move = a3.replace('3_attack_1','2_move')
			find = self.chkEmpty(move, moves)
			if find:
				idle = a3.replace('3_attack_1','1_idle')
				# print(idle)
				find = self.chkEmpty(idle, idles)

				if not find:					
					#copy last picture in 1_idle to 2_move, 3_attack_1, 4_attack_2, 5_attack_3
					src = scanFile(idle)[-1]
					dests = ['2_move', '3_attack_1', '4_attack_2', '5_attack_3']
					# print(dests)
					for dest in dests:
						copyFile(src, src.replace('1_idle', dest))

				die = a3.replace('3_attack_1','6_die_1')
				find = self.chkEmpty(die, dies)
				# print(die,find)
				if not find:
					#copy last picture in 6_die_1 to 7_die_2,  8_die_3					
					src = scanFile(die)[-1]
					copyFile(src, src.replace('6_die_1', '7_die_2'))
					copyFile(src, src.replace('6_die_1', '8_die_3'))

			#2_move is not empty
			else:
				die = a3.replace('3_attack_1','6_die_1')
				find = self.chkEmpty(die,dies )
				if not find:
					src = scanFile(die)[-1]
					copyFile(src, src.replace('6_die_1', '7_die_2'))
					copyFile(src, src.replace('6_die_1', '8_die_3'))

				#copy last picture in 1_idle to 2_move, 3_attack_1, 4_attack_2, 5_attack_3
				src = scanFile(move)[-1]
				dests = ['3_attack_1', '4_attack_2', '5_attack_3']
				# print(dests)
				for dest in dests:
					copyFile(src, src.replace('2_move', dest))

				idle = a3.replace('3_attack_1','1_idle')
				find = self.chkEmpty(idle, idles)
				if find:
					dest = src.replace('2_move', '1_idle')
					copyFile(src, dest)
		
		#3_attack_1 is not empty
		# print(a31exits)
		for a31 in a31exits:
			# print(a31)
			a31firstpng = scanFile(a31)[0]
			idle = a31.replace('3_attack_1','1_idle')
			find = self.chkEmpty(idle, idles)

			#1_idle empty
			if find:
				# print('find 1_idle')
				move = a31.replace('3_attack_1','2_move')
				find = self.chkEmpty(move, moves)
				if find:
					src = a31firstpng
					copyFile(src, src.replace('3_attack_1','1_idle'))
				else:
					src = scanFile(move)[0]
					copyFile(src, src.replace('2_move', '1_idle'))
				# continue

			#2_move is empty
			move = a31.replace('3_attack_1','2_move')
			find = self.chkEmpty(move, moves)
			if find:
				# print('find move')
				copyFiles(a31.replace('3_attack_1','1_idle'), move, recur=False)
				# continue

			#4_attack_2 or 5_attack_3 is empty
			a42 = a31.replace('3_attack_1','4_attack_2')
			a53 = a31.replace('3_attack_1','5_attack_3')
			f42 = self.chkEmpty(a42, attacks)
			f53 = self.chkEmpty(a53, attacks)
			if f42:
				# src = a31firstpng
				copyFiles(a31, a42,recur=False)
				# continue
			if f53:
				copyFiles(a31, a53, recur=False)
				# continue
			
			#6_die_1 is not empty
			die = a31.replace('3_attack_1','6_die_1')
			find = self.chkEmpty(die, dies)
			if not find:
				src = scanFile(die)[-1]
				die7 = src.replace('6_die_1','7_die_2')
				die8 = src.replace('6_die_1','8_die_3')
				copyFile(src, die7)
				copyFile(src, die8)
				# continue

			#6_die_1, 7_die_2 , 8_die_3 is empty
			d6 = a31.replace('3_attack_1','6_die_1')
			d7 = a31.replace('3_attack_1','7_die_2')
			d8 = a31.replace('3_attack_1','8_die_3')
			f6 = self.chkEmpty(d6,dies)
			f7 = self.chkEmpty(d7,dies)
			f8 = self.chkEmpty(d8,dies)
			if f6 and f7 and f8:
				src =a31firstpng
				copyFile(src, src.replace('3_attack_1','6_die_1'))
				copyFile(src, src.replace('3_attack_1','7_die_2'))
				copyFile(src, src.replace('3_attack_1','8_die_3'))
		# exit()