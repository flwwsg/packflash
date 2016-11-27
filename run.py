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
from code.cleanprocess import Cleanprocess

def run(pack, jsfl, ttdir, fdir, flock, pipeout):
	try:
		pack.runAll(jsfl, ttdir, fdir, flock)
	except PackExp as e:
		e.wlog()
	finally:
		msg = str(os.getpid())+' finish'
		os.write(pipeout, msg.encode())	
	
def process(pprocess, filenames, pipes, flock):
	tsrcdir = pprocess.tspath
	ttdir = pprocess.ttpath
	jsfl = pprocess.kpjsfl
	finalpath = pprocess.finalpath

	tmpsrcnames = scanDir(tsrcdir)
	for modpath in tmpsrcnames: #commandoxx, factoryxx ...
		subdir = scanDir(modpath)
		count = len(subdir)
		tmp = baseName(modpath)
		filenames.append(tmp)
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
		pipein, pipeout = os.pipe()
		newthread = genThread(run, pack, jsfl, ttdir, finalpath, flock, pipeout)
		pipes.append(pipein)
		# run(pack, jsfl, ttdir, finalpath, flock)

filenames = []
pipes = []

try:
	startime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	pprocess = Preprocess()
	pprocess.preprocess()
	process(pprocess, filenames, pipes, FLOCK)

	#wait for thread exited
	for pipein in pipes:
		msg = os.read(pipein, 32).decode()
		print(msg)
	Cleanprocess.cleanprocess(pprocess.tpath, startime, ','.join(filenames))
except PackExp as e:
	e.wlog()

