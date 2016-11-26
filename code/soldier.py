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
		self.subdirs = ['1_2','2_0','3_1','4_7','5_3','6_6','7_5','8_4']
		self.dealPng(mod)
		Packer.__init__(self, 'soldiers',mod)

	def dealPng(self, src):
		newemptys=self.getEmpty(src)
		newexists = nonemptyDir(src)
		# print(newemptys, newexists)

		if not newemptys:
			return
		moves = list()  #2_move is empty
		attacks = list() #attack is empty
		dies = list()  #die is empty
		for item in newemptys:
			if item.find('2_move') != -1:
				moves.append(item)
				continue
			if item.find('3_attack_1') !=-1 or item.find('4_attack_2') != -1 or item.find('5_attack_3') != -1:
				attacks.append(item)
				continue
			if item.find('7_die_2') != -1 or item.find('8_die_3') != -1:
				dies.append(item)
				continue

		#attack is empty
		for attack in attacks:
			adn = baseName(attack)
			move = attack.replace(adn, '2_move')
			find = self.chkEmpty(move, moves)
			if not find:
				lastpng = scanFiles(move)[-1]
				# print(lastpng)
				dest =attack+'/'+baseName(lastpng)
				# print(dest)
				copyFile(lastpng, dest)
				
		for die in dies:
			bn = baseName(die)
			die1 = die.replace(bn,'6_die_1')
			copyFiles(die1, die,recur=False)
