#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''helper function for animation run'''
import os 
import shutil
import sys
from code.sendmail import *

def mkDir(paths):
	if isinstance(paths,str):
		paths = [paths]
	for path in paths:
		if os.path.exists(path):
			continue
		else:
			os.makedirs(path)

def rmDir(dirname):
	if not os.path.exists(dirname):
		return None
	shutil.rmtree(dirname)
	
#
def scanFiles(root,withpath=True):
	name = list()
	for dirs, subdirs, fns in os.walk(root):
		for fn in fns:
			if withpath:
				fullpath = os.path.join(dirs,fn)
			else:
				fullpath = fn
			name.append(fullpath)
	return name;

def scanFile(root, withpath=True):
	dirs = os.listdir(root)
	name = list()
	for file in dirs:
		tmp = os.path.join(root, file)
		isdir = os.path.isdir(tmp)
		if not isdir and withpath:
			name.append(tmp)
		elif not isdir and not withpath:
			name.append(file)
	return name

def scanDir(root, withpath=True):
	names = list()
	if not os.path.exists(root):
		return None
	dirs = os.listdir(root)

	for file in dirs:
		tmp = os.path.join(root, file)
		isdir = os.path.isdir(tmp)
		if isdir and withpath:
			names.append(tmp)
		elif isdir and not withpath:
			names.append(file)
	return names

def copyFiles(src, dest, recur=True,ignore=None):
	if recur:
		shutil.copytree(src, dest, ignore=ignore)
	else:
		dirs = os.listdir(src)
		for file in dirs:
			tmp = os.path.join(src, file)
			if not os.path.isdir(tmp):
				shutil.copy(tmp,dest)
				
def copyFile(src, dest):
	shutil.copyfile(src, dest)

def genPath(root, path):
	return os.path.join(root, path)

def chkType(fn):
	types = dict(ui='gui',ff='mobs',jz='building', tx='effects',zf='units')
	num = -2
	ch = fn[num:]
	if ch in types.keys():
		return types[ch]
	else:
		return False

def baseName(path):
	return os.path.basename(path)

def emptyDir(path):
	empty = list()
	for dirs, subdirs, fnames in os.walk(path):
		if not subdirs and not fnames:
			empty.append(dirs)
	return empty

def nonemptyDir(path):
	nonempty = list()
	for dirs, subdirs, fnames in os.walk(path):
		if fnames:
			nonempty.append(dirs)
	return nonempty


def dirName(path):
	return os.path.dirname(path)

def countDir(root):
	n = 0
	if not os.path.exists(root):
		return n
	dirs = os.listdir(root)
	for file in dirs:
		tmp = os.path.join(root, file)
		if os.path.isdir(tmp):
			n += 1
	return n

def countFile(root):
	n = 0
	if not os.path.exists(root):
		return n
	dirs = os.listdir(root)
	for file in dirs:
		tmp = os.path.join(root, file)
		if not os.path.isdir(tmp):
			n += 1
	return n

def indent(elem, level=0):
	i = "\n" + level*"  "
	j = "\n" + (level-1)*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for subelem in elem:
			indent(subelem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = j
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = j
	return elem  

def smail(receiver,subject,fname=None,mbody=None):
	for addr in receiver:
		sendMail(receiver=addr,subject=subject,fname=fname,mbody=mbody)

