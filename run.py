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

# def runflashcc(pipein):
# 	flag = os.read(pipein, 1024)
# 	tmp = flag.decode('utf-8')
# 	flist = tmp.split(',')
# 	for fname in flist:
# 		# print(fname)
# 		os.system(fname)

def run(pack, jsfl, ttdir, fdir, pipeout, pipein):
	paths = pack.runAll(jsfl, ttdir, fdir)
	print(pack.modname+' threading finish')

	msg = ''
	first = True
	for path in paths:
		if first:
			tmp = path
			first = False
		else:
			tmp = ','+path
		msg += tmp
	os.write(pipeout, msg.encode())
	# runflashcc(pipein)

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
# threads = []
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
		newthread = threading.Thread(target=run,args=(pack,jsfl, ttdir, fdir, pipeout, pipein, )).start()
		# threads.append(newthread)
		pipes.append(pipein)
	except PackExp as e:
		e.wlog()

fnames = []
for pipein in pipes:
	flag = os.read(pipein, 1024)
	tmp = flag.decode('utf-8')
	fnames.append(tmp)
	print(tmp)

for fname in fnames:
	flist = fname.split(',')
	for jsfl in flist:
		print(jsfl)
		os.system(jsfl)
		swf = jsfl.replace('.jsfl', '.swf')
		fla = jsfl.replace('.jsfl', '.fla')

# cleanprocess(tpath, filename)
