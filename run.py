#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from code.packHelper import *
from code.soldier import Soldier
from code.building import Building
from code.head import Head
from code.dhead import DHead
from code.body import Body
from code.dbody import DBody
from code.bsoldier import BSoldier
from code.packexp import *
from code.preprocess import Preprocess
from code.misc import genThread, FLOCK
from code.cleanprocess import Cleanprocess

def run(pack, jsfl, ttdir, fdir, flock, pipeout,modpath):
	try:
		if not pack:
			raise PackNotSupported(modpath)
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
		style = modpath[-2:]
		count = len(subdir)
		tmp = baseName(modpath)
		filenames.append(tmp)
		bn = tmp.split('#')[-1]
		dota = bn[:4]

		if style == 'jz':
			if count == 5:
				print('Processing building')
				pack = Building(modpath)
			elif count == 1:
				print('Processing building-soldier')
				pack = BSoldier(modpath)
			else:
				pack = False
		elif count == 5:
			print('Processing soldier')
			pack = Soldier(modpath)
		elif count==17:
			if dota == 'dota':
				print('Processing dota Head')
				pack = DHead(modpath)
			else:
				print('Processing Head')
				pack = Head(modpath)
		elif count == 9:
			if dota == 'dota':
				print('Processing dota Body')
				pack = DBody(modpath)
			else:
				print('Processing Body')
				pack = Body(modpath)
		else:
			pack = False
		pipein, pipeout = os.pipe()
		newthread = genThread(run, pack, jsfl, ttdir, finalpath, flock, pipeout,modpath)
		pipes.append(pipein)
		# run(pack, jsfl, ttdir, finalpath, flock)

filenames = []
pipes = []

try:
	startime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	pprocess = Preprocess()
	clean = Cleanprocess()
	pprocess.preprocess()
	process(pprocess, filenames, pipes, FLOCK)

	#wait for thread exited
	for pipein in pipes:
		msg = os.read(pipein, 32).decode()
		print(msg)
	clean.cleanprocess(startime, ','.join(filenames))
except PackExp as e:
	e.wlog()