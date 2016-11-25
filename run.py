#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''run.py'''

from code.preprocess import preprocess
from code.cleanprocess import cleanprocess
import code.packHelper as helper
from code.packer import Packer
from code.soldier import Soldier
from code.packdata import PackData
from code.building import Building
from code.head import Head
from code.dhead import DHead
from code.body import Body
from code.dbody import DBody
from code.packexp import *
import threading

def run(pack, jsfl, ttdir, fdir, pipeout):
	pack.runAll(jsfl, ttdir, fdir)
	print(pack.modname+' threading finish')
	msg = 'ok'.encode()
	os.write(pipeout, msg)

def init():
	try:
		tmp = preprocess() 
	except PackExp as e:
		e.wlog()
		exit(e.logs) 
	return tmp

tmp = init()
tsrcdir = tmp['tsrcdir'] 
ttdir = tmp['ttdir'] 
jsfl = tmp['kpjsfl'] 
srcdir = tmp['srcdir']
fdir = tmp['fdir']
tpath = tmp['tpath']
filename = ''
threads = []
pipes = []

tmpsrcnames = helper.scanDir(tsrcdir)
for modpath in tmpsrcnames: #commandoxx, factoryxx ...
	pipein, pipeout = os.pipe()

	subdir = helper.scanDir(modpath)
	count = len(subdir)
	tmp = helper.baseName(modpath)
	filename = tmp + ',' + filename
	bn = tmp.split('#')[-1]
	dota = bn[:4]
	# print(modpath, style,count)
	if count==8:
		print('Processing soldier')
		pack = Soldier(modpath)
	elif count == 5:
		print('Processing building')
		pack = Building(modpath)
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
	try:
		newthread = threading.Thread(target=run,args=(pack,jsfl, ttdir, fdir, pipeout, )).start()
		threads.append(newthread)
		pipes.append(pipein)
	except PackExp as e:
		e.wlog()

for pipein in pipes:
	flag = os.read(pipein,32)

cleanprocess(tpath, filename)
