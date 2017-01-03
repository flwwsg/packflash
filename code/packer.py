#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# import os 
from code.packHelper import *
from PIL import Image, ImageDraw
import xml.etree.ElementTree as et
from code.packdata import PackData
from code.cleanprocess import Cleanprocess
from code.packexp import *
from time import sleep

class Packer(object):
	"""packing pictures for flash"""
	def __init__(self, modtype,fpath, modnamelocation=-1):
		self.type = modtype
		self.fpath = fpath
		self.modnamelocation = modnamelocation
		self.formatDir()
		self.fullname = '-'.join([self.modname, self.modtype, self.type])

		#rename files
	def formatDir(self):
		dirs = scanDir(self.fpath)
		path = self.fpath
		path = baseName(path)
		newtype = chkType(path)
		if not newtype:
			raise PackNotSupported(self.fpath)
		newpath = path.split('#')[self.modnamelocation].split('-')[0]
		newpath = newpath+'-'+newtype

		# for example modname = commando , modtype = mobs
		self.modname = newpath.split('-')[0]
		self.modtype = newpath.split('-')[1]

		subdirs = scanDir(self.fpath)
		# print(subdirs)
		index = 11
		for spath,name in zip(subdirs,self.subdirs):
			bname = baseName(spath)
			newname = genPath(self.fpath,name)
			# print(spath, newname)
			#make new name
			fnames = scanFiles(spath)
			for file in fnames:
				newfn = dirName(file)
				tmp = baseName(file)
				if tmp == 'background.png':
					continue
				if index < 100:
					n = "00"+str(index)
				elif index <1000:
					n = "0"+str(index)
				else:
					n = str(index)
				os.rename(file, genPath(newfn, 'new'+n+'.png'))
				index += 1

			if spath == newname:
				continue
			os.rename(spath, newname)

		#subdir = 1_2, xx , status = 1_idle
	def getEmptyStatus(self, subdir):
		status = scanDir(subdir,False)
		status = set(status)
		diffs = self.fstatus - status
		return diffs

	def mv2finalSource(self, fdir, jsfl, fname=None):
		if not fname:
			fname = self.modname
		style = self.modtype
		dirname = fdir+'/'+style+'/'+self.type
		swfsrc = jsfl+'/'+fname+'.swf'		
		flasrc = jsfl+'/'+fname+'.fla'		
		swfdest = dirname+'/'+fname+'.swf'
		fladest = dirname+'/'+fname+'.fla'
		mkDir(dirname)
		# print(src, dest)
		copyFile(swfsrc,swfdest)
		copyFile(flasrc,fladest)
		return swfdest
		
	def runAll(self, jsfl, ttdir, fdir, flock):
		out = ttdir+'/'+baseName(self.fpath)
		self.ttpack(self.fpath,out)       #xmlpaths = dict(1_2=xx.xml)
		cutout =out+ '_cut'

		#cutting small picture saved at tmp/texture/xxx_cut from picture processed by texture on tmp/texture/xxx
		self.ttcutimg(out)  

		#执行扫描并生成{self.fullname}xml  
		pdata = PackData(cutout)
		pdata.countPics()
		pdata.getitems(out, self.replace)
		pdata.genjsfl(self.fullname,jsfl)
		pdata.genroot(self.modname)
		pdata.witem()

		for subdir in pdata.subdir:			
			pdata.wbody(pdata, subdir, self.replace)
		fname = genPath(jsfl,self.fullname+'.xml')
		pdata.savexml(fname)
		
		clean = Cleanprocess()
		with flock:
			os.system(fname[:-3]+'jsfl')
			location = self.mv2finalSource(fdir, jsfl)
			if not os.path.exists(location):
				raise SWFNotFound(location)
			clean.copy2SVN(location, self.type, self.modtype,self.fpath)
			sleep(10)

	@classmethod
	def ttpack(self,src,out):     #src directory name such sas 1_2 , 2_x ...
		sfiles = scanDir(src)
		for file in sfiles:
			fname = baseName(file)
			cmd = "TexturePacker --max-width 4096 --max-height 4096 --pack-mode Best --size-constraints AnySize --data %s/%s.xml --format sparrow --sheet %s/%s.png %s" % (
					out, fname, out, fname, file)
			output = os.popen(cmd).read()        #must using read

	@classmethod
	def ttcutimg(self,src,cutout=None):
		sfiles = scanFile(src)
		bnsrc = baseName(src)
		# print(src, sfiles)
		pics = list()
		for file in sfiles:
			# print(file)
			if file[-3:] == 'png':
				pics.append(dict(png=file, xml=file[:-3]+'xml'))
		for pic in pics:
			tree = et.parse(pic['xml'])
			root = tree.getroot()
			for subtt in root:
				x = subtt.get('x')
				y = subtt.get('y')
				width = subtt.get('width')
				height = subtt.get('height')
				name = subtt.get('name')
				name += '.png'
				name =genPath( pic['png'][:-4],name)
				if not cutout:
					out = name.replace(bnsrc, bnsrc+'_cut' )
				else:
					out = name.replace(bnsrc, cutout)
				data = dict()
				data['x'] = int(x)
				data['y'] = int(y)
				data['width'] = int(width)
				data['height'] = int(height)
				self.cutimg(data, pic['png'], out)

	@classmethod
	def cutimg(self,data, imgfile, out):
		x = data['x'] 
		y = data['y']
		width = data['width']
		height = data['height']

		with Image.open(imgfile) as img:
			img2 = img.crop((x, y, x+width, y+height))
			outdir = dirName(out)
			mkDir(outdir)
			img2.save(out)

	@classmethod
	def creatTransparentPng(self, out):
		img = Image.new('RGBA', (512, 512))
		img.save(out, 'png')