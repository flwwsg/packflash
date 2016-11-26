#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from code.packHelper import *
from code.soldier import Soldier
from code.building import Building
from code.head import Head
from code.dhead import DHead
from code.body import Body
from code.dbody import DBody
from code.packexp import *
from code.preprocess import Preprocess
from code.misc import genThread, FLOCK

def run(pack, jsfl, ttdir, fdir, flock):
	pack.runAll(jsfl, ttdir, fdir)

def process(pprocess, flock):
	tsrcdir = pprocess.tspath
	ttdir = pprocess.ttpath
	jsfl = pprocess.kpjsfl
	tpath = pprocess.tpath
	finalpath = pprocess.finalpath

	filename = ''
	tmpsrcnames = scanDir(tsrcdir)
	for modpath in tmpsrcnames: #commandoxx, factoryxx ...
		subdir = scanDir(modpath)
		count = len(subdir)
		tmp = baseName(modpath)
		filename = tmp + ',' + filename
		bn = tmp.split('#')[-1]
		dota = bn[:4]
		# print(modpath,count)
		if count==5:
			print('Processing building')
			pack = Building(modpath)
		elif count == 8:
			print('Processing soldier')
			pack = Soldier(modpath)
		elif count==32:
			if dota == 'dota':
				print('Processing dota Head')
				pack = DHead(modpath)
			else:
				print('Processing Head')
				pack = Head(modpath)
		elif count == 16:
			if dota == 'dota':
				print('Processing dota Body')
				pack = DBody(modpath)
			else:
				print('Processing Body')
				pack = Body(modpath)
		# genThread(run, pack, jsfl, ttdir, finalpath, flock)
		run(pack, jsfl, ttdir, finalpath, flock)
# cleanprocess(tpath, filename)

pprocess = Preprocess()
pprocess.preprocess()
process(pprocess,FLOCK)

# try:
# 	pprocess = Preprocess()
# 	pprocess.preprocess()
# 	process(pprocess)
# except PackExp as e:
# 	e.wlog()