#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''body.py'''

from code.head import Head
from code.packer import Packer
import code.packHelper as helper

class Body(Packer):
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
		Packer.__init__(self,'vehicles_body', mod)


	def dealPng(self, dirsrc):
		newemptys = self.getEmpty(dirsrc)
		exists = helper.nonemptyDir(dirsrc)

		a31exits= list()
		for exist in exists:
			if exist.find('3_attack_1') != -1:
				a31exits.append(exist)
		# print(a31exits)
		# exit()

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
					src = helper.scanFile(idle)[-1]
					dests = ['2_move', '3_attack_1', '4_attack_2', '5_attack_3']
					# print(dests)
					for dest in dests:
						helper.copyFile(src, src.replace('1_idle', dest))

				die = a3.replace('3_attack_1','6_die_1')
				find = self.chkEmpty(die, dies)
				# print(die,find)
				if not find:
					#copy last picture in 6_die_1 to 7_die_2,  8_die_3					
					src = helper.scanFile(die)[-1]
					helper.copyFile(src, src.replace('6_die_1', '7_die_2'))
					helper.copyFile(src, src.replace('6_die_1', '8_die_3'))

			#2_move is not empty
			else:
				die = a3.replace('3_attack_1','6_die_1')
				find = self.chkEmpty(die,dies )
				if not find:
					src = helper.scanFile(die)[-1]
					helper.copyFile(src, src.replace('6_die_1', '7_die_2'))
					helper.copyFile(src, src.replace('6_die_1', '8_die_3'))

				#copy last picture in 1_idle to 2_move, 3_attack_1, 4_attack_2, 5_attack_3
				src = helper.scanFile(move)[-1]
				dests = ['3_attack_1', '4_attack_2', '5_attack_3']
				# print(dests)
				for dest in dests:
					helper.copyFile(src, src.replace('2_move', dest))

				idle = a3.replace('3_attack_1','1_idle')
				find = self.chkEmpty(idle, idles)
				if find:
					dest = src.replace('2_move', '1_idle')
					helper.copyFile(src, dest)
		
		#3_attack_1 is not empty
		
		for a31 in a31exits:
			a31firstpng = helper.scanFile(a31)[0]
			idle = a31.replace('3_attack_1','1_idle')
			find = self.chkEmpty(idle, idles)

			#1_idle empty
			if find:
				move = a31.replace('3_attack_1','2_move')
				find = self.chkEmpty(move, moves)
				if find:
					src = a31firstpng
					helper.copyFile(src, src.replace('3_attack_1', '1_idle'))
				else:
					src = helper.scanFile(move)[0]
					helper.copyFile(src, src.replace('2_move','1_idle'))
				# continue

			#2_move is empty
			move = a31.replace('3_attack_1','2_move')
			find = self.chkEmpty(move, moves)
			if find:
				helper.copyFiles(a31.replace('3_attack_1','1_idle'), move, recur=False)
				# continue

			#4_attack_2 or 5_attack_3 is empty
			a42 = a31.replace('3_attack_1','4_attack_2')
			a53 = a31.replace('3_attack_1','5_attack_3')
			f42 = self.chkEmpty(a42, attacks)
			f53 = self.chkEmpty(a53, attacks)
			if f42 and f53:
				src = a31firstpng
				helper.copyFile(src, a42)
				helper.copyFile(src, a53)
				# continue
			
			#6_die_1 is not empty
			die = a31.replace('3_attack_1','6_die_1')
			find = self.chkEmpty(die, dies)
			if not find:
				src = helper.scanFile(die)[-1]
				die7 = a31.replace('3_attack_1','7_die_2')
				die8 = a31.replace('3_attack_1','8_die_3')
				helper.copyFile(src, die7)
				helper.copyFile(src, die8)
				# continue

			#6_die_1, 7_die_2 , 8_die_3 is empty
			d6 = a31.replace('3_attack_1','6_die_1')
			d7 = a31.replace('3_attack_1','7_die_2')
			d8 = a31.replace('3_attack_1','8_die_3')
			f6 = self.chkEmpty(d6,dies)
			f7 = self.chkEmpty(d7,dies)
			f7 = self.chkEmpty(d8,dies)
			if f6 and f7 and f8:
				src =a31firstpng
				helper.copyFile(src, d6)
				helper.copyFile(src, d7)
				helper.copyFile(src, d8)