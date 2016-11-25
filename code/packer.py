#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os 
import code.packHelper as helper
from PIL import Image, ImageDraw
import xml.etree.ElementTree as et
from code.packdata import PackData
from code.cleanprocess import copy2SVN
from code.packexp import *

class Packer(object):
	"""packing pictures for flash"""
	def __init__(self, types,fpath):
		self.type = types
		self.fpath = fpath
		self.formatDir(fpath)

	def ttpack(self,src,out):     #src directory name such sas 1_2 , 2_x ...
		sfiles = helper.scanDir(src)
		for file in sfiles:
			fname = helper.baseName(file)
			if fname in self.replace.keys():
				continue
			cmd = "TexturePacker --max-width 4096 --max-height 4096 --pack-mode Best --size-constraints AnySize --data %s/%s.xml --format sparrow --sheet %s/%s.png %s" % (
					out, fname, out, fname, file)
			# print(file, fname, cmd)
			output = os.popen(cmd).read()        #must using read

	def ttcutimg(self,src):
		sfiles = helper.scanFile(src)
		bnsrc = helper.baseName(src)
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
				name =helper.genPath( pic['png'][:-4],name)
				out = name.replace(bnsrc, bnsrc+'_cut' )
				data = dict()
				data['x'] = int(x)
				data['y'] = int(y)
				data['width'] = int(width)
				data['height'] = int(height)
				self.cutimg(data, pic['png'], out)

	def cutimg(self,data, imgfile, out):
		x = data['x'] 
		y = data['y']
		width = data['width']
		height = data['height']

		with Image.open(imgfile) as img:
			img2 = img.crop((x, y, x+width, y+height))
			outdir = helper.dirName(out)
			helper.mkDir(outdir)
			img2.save(out)

	# def creatTransparentPng(self, out):
	#     img = Image.new('RGBA', (180, 180))
	#     draw = ImageDraw.Draw(img)
	#     draw.rectangle((0, 0, 180, 180))
	#     img.save(out, 'png')

	def getEmpty(self, mod):
		emptys = helper.emptyDir(mod)
		newemptys = list()

		for item in emptys:
			find = False
			for k in self.replace.keys():
				if item.find(k) != -1:
					find = True
					break
			if not find:
				newemptys.append(item)
		return newemptys

	def chkEmpty(self, name, elist):
		for l in elist:
			if l==name:
				return True

		return False

	#rename files
	def formatDir(self,fpath):
		dirs = helper.scanDir(fpath)
		path = fpath
		path = helper.baseName(path)
		newtype = helper.chkType(path)
		newpath = path.split('#')[0].split('-')[0]
		newpath = newpath+'-'+newtype

		# for example modname = commando , modtype = mobs
		self.modname = newpath.split('-')[0]
		self.modtype = newpath.split('-')[1]

		subdirs = helper.scanDir(fpath)
		# print(subdirs)
		index = 11
		for spath,name in zip(subdirs,self.subdirs):
			bname = helper.baseName(spath)
			newname = helper.genPath(fpath,name)
			# print(spath, newname)
			#make new name
			fnames = helper.scanFiles(spath)
			for file in fnames:
				newfn = helper.dirName(file)
				tmp = helper.baseName(file)
				if tmp == 'background.png':
					continue
				if index < 100:
					n = "00"+str(index)
				elif index <1000:
					n = "0"+str(index)
				else:
					n = str(index)
				os.rename(file, helper.genPath(newfn, 'new'+n+'.png'))
				index += 1
			os.rename(spath, newname)

	def mv2finalSource(self, fdir, jsfl, fname=None):
		if not fname:
			fname = self.modname
		style = self.modtype
		dirname = fdir+'/'+style+'/'+self.type
		swfsrc = jsfl+'/'+fname+'.swf'		
		flasrc = jsfl+'/'+fname+'.fla'		
		swfdest = dirname+'/'+fname+'.swf'
		fladest = dirname+'/'+fname+'.fla'
		helper.mkDir(dirname)
		# print(src, dest)
		helper.copyFile(swfsrc,swfdest)
		helper.copyFile(flasrc,fladest)
		return swfdest

	def runItem(self, root, titem, pdata, pngnums, pngxy, dirname, cutpath, index=0):
		self.nextpic =PackData.wlabel(dirname,pngnums,pdata.status, self.replace,titem, index)
		backpngs = PackData.wpics(dirname, pngxy, self.replace, cutpath, titem, index+1)
		if backpngs:
			PackData.wbackground(backpngs, titem)
		

	def runOnce(self, pdata, pngnums, pngxy, dirname, modname, jsfl, cutpath ):
		pdata.genjsfl(modname,jsfl)
		root = PackData.genroot(modname)
		titem = PackData.witem(root)
		self.runItem(root, titem,pdata, pngnums, pngxy, dirname, cutpath)
		PackData.savexml(root,helper.genPath(jsfl, modname+'.xml'))
		fname = helper.genPath(jsfl, modname+'.jsfl')
		return fname
		# os.system(fname)

	def runAll(self, jsfl, ttdir, fdir):
		out = ttdir+'/'+helper.baseName(self.fpath)
		self.ttpack(self.fpath,out)       #xmlpaths = dict(1_2=xx.xml)
		cutout =out+ '_cut'

		#cutting small picture saved at tmp/texture/xxx_cut from picture processed by texture on tmp/texture/xxx
		self.ttcutimg(out)  

		#执行扫描并生成xml
		pdata = PackData(cutout)
		pngnums =PackData.countPics(cutout,pdata.subdir,pdata.status)
		pngxy = PackData.getitems(out,pdata.subdir,self.replace)

		#generate jsfl file
		pdata.genjsfl(self.modname,jsfl)
		root = PackData.genroot(self.modname)
		titem = PackData.witem(root)

		self.nextpic = 0
		for subdir in pdata.subdir:
			self.runItem(root, titem, pdata, pngnums, pngxy, subdir, cutout,self.nextpic)

		PackData.savexml(root,helper.genPath(jsfl, self.modname+'.xml'))
		fname = helper.genPath(jsfl, self.modname+'.jsfl')
		# os.system(fname)
		
		# location = self.mv2finalSource(fdir, jsfl)
		# copy2SVN(location, self.modtype, self.type)
		return fname

