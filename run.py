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
from code.cleanprocess import cleanprocess

def run(pack, jsfl, ttdir, fdir, flock, pipeout):
	pack.runAll(jsfl, ttdir, fdir, flock)
	msg = str(os.getpid())+' finish'
	os.write(pipeout, msg.encode())


def process(pprocess, filenames, threads, flock, pipeout):
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
		newthread = genThread(run, pack, jsfl, ttdir, finalpath, flock, pipeout)
		threads.append(newthread)
		# run(pack, jsfl, ttdir, finalpath, flock)

threads = []
filenames = []
pipein, pipeout = os.pipe()

try:
	pprocess = Preprocess()
	pprocess.preprocess()
	process(pprocess, filenames, threads, FLOCK, pipeout)

	#wait for thread exited
	for thread in threads:
		msg = os.read(pipein, 32).decode()
		print(msg)
	cleanprocess(pprocess.tpath, ','.join(filenames))
except PackExp as e:
	e.wlog()

