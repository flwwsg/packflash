#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''packdata.py'''

from code.packHelper import *
import xml.etree.ElementTree as et

PICQUALITY = "80"
BACKQUALITY = "80"
class PackData(object):
	"""docstring for PackData"""
	def __init__(self, modpath):
		data = self.getachive(modpath)
		self.subdir = data['subdir']
		self.status = data['status']
		self.modpath = modpath
		self.lindex = 0
		self.pindex = 1

	def getachive(self,modpath):
		dirs = scanDir(modpath, withpath=False)

		path = genPath(modpath, dirs[0])
		status = scanDir(path,withpath=False)
		files = scanFile(path,withpath=False)
		return dict(subdir=dirs, status=dict(dir=status, file=files))

	# def wxml(self, replace):
	# 	root = self.genroot()
	# 	titem = self.witem(root)
	# 	self.wlabel(replace, titem)
	# 	self.wpics(replace, titem)

	# 	root = indent(root)
	# 	et.ElementTree(root).write(self.jsfl+'/'+self.xmlname)
	# 	return self.jsfl+'/'+self.xmlname.replace('.xml','.jsfl')


	# @classmethod
	def countPics(self): #modpath = command xxx
		modpath = self.modpath
		subdir = self.subdir
		status = self.status
		pngnums =dict()
		# print(dirs)
		for dirname in subdir:      # subdir = 1_2 , xx
			path = modpath +'/'+ dirname
			newstatus = dict()

			newstatus['file'] = len(status['file'])

			for sdir in status['dir']: #sdir = 1_idle
				spath = path + '/' + sdir
				file = scanFile(spath)
				newstatus[sdir] = len(file)

				pngnums[dirname] =newstatus
		self.pngnums = pngnums

	# @classmethod
	def getitems(self, ttxml,replace):
		tmp = scanFile(ttxml)
		xmlpath = dict()
		for i in tmp:
			if i[-3:] == 'xml':
				ibn = baseName(i)
				xmlpath[ibn[:-4]]=i

		pngxy = dict()
		self.subdir.extend(sorted(replace.keys()))

		for dirname in self.subdir:
			if dirname in replace.keys():
				newdirname = replace[dirname]
			else:
				newdirname = dirname
			# print(newdirname, dirname)
			pngxy[dirname] = PackData.getxy(xmlpath[newdirname])
		self.pngxy = pngxy

		#pngnums like pngnums['1_2']{'file':[], '1_idle': 24}

	def wlabel(self, dirname, replace, xitem):
		layer = et.SubElement(xitem,'layer',{'name':'label'})
		pre = dirname.split('_')[-1]
		if pre[0] == '0' and pre != '0':
			pre = pre[1:]
		if dirname in replace.keys():
			item = self.pngnums[replace[dirname]]
		else:
			item = self.pngnums[dirname]

		for k in self.status['dir']:    #status['dir'] =['1_2', 'x_x' ...]
			v = item[k]
			name = pre+k[1:]
			et.SubElement(layer, 'frame',  {'start_index':str(self.lindex+1), 
											'end_index': str(self.lindex+v), 
											'label':name})
			self.lindex += v
		

	# #pngxy like pngxy['1_2'] [{'xname':'xx', 'xpath':'1_idle','x':x, 'y':y}]
	
	def wpics(self, dirname, replace, xitem):
		layer = et.SubElement(xitem,'layer',{'name':'pics'})

		scalex = False
		backpngs =list()
		if dirname in replace.keys():
			dirname = replace[dirname]
			scalex = True
		for item in self.pngxy[dirname]:
			backpng = dict()
			xname = item['xname']
			x = item['x']
			y = item['y']
			xpath = item['xpath']
			width = item['width']
			height = item['height']
			path = self.modpath +'/'+ dirname
			

			if xname != 'background':
				path = path +'/'+ xpath
				path = path +'/'+ xname+'.png'
				if not scalex:
					et.SubElement(layer, 'frame', {'quality':PICQUALITY, 'x':str(x), 'y':str(y), 
						'source_path':path, 
						'start_index':str(self.pindex), 'end_index':str(self.pindex)})
				else:
					et.SubElement(layer, 'frame', {'quality':PICQUALITY, 'x':str(x*(-1)-width), 'y':str(y), 
						'source_path':path, 'scaleX':'-1', 
						'start_index':str(self.pindex), 'end_index':str(self.pindex)})
			else:
				backpng['x'] = x
				backpng['y'] = y
				backpng['width'] = width
				backpng['height'] = height
				backpng['path'] = path +'/'+ xname+'.png'
				backpng['count'] = self.pindex-1
				backpngs.append(backpng)

			self.pindex += 1

		self.backpngs = backpngs

	def wbackground(self,xitem):
		layer = et.SubElement(xitem,'layer',{'name':'background'})
		index = 0

		for backpng in self.backpngs:
			et.SubElement(layer, 'frame', {'quality':BACKQUALITY, 'x':str(backpng['x']), 'y':str(backpng['y']), 
						'source_path':backpng['path'], 
						'start_index':str(index+1), 'end_index':str(backpng['count'] + index)})
			index += backpng['count']


	@classmethod
	def getxy(self, path):
		ttxml = et.parse(path)
		root = ttxml.getroot()

		tmplist = list()
		for subtt in root:
			pngpath = subtt.get('name')
			# print(pngpath)
			if 'background' in pngpath:
				xname = 'background'
				xpath = pngpath
			else:
				tmp = pngpath.split('/')
				xpath, xname = tmp[0], tmp[1]

			frameWidth = int(subtt.get('frameWidth'))
			frameHeight = int(subtt.get('frameHeight'))
			frameX = int(subtt.get('frameX'))
			frameY = int(subtt.get('frameY'))
			width = int(subtt.get('width'))
			height = int(subtt.get('height'))
			x = abs(frameX)-frameWidth/2
			y = abs(frameY)-frameHeight/2
			dd = dict(xname=xname, xpath=xpath, x=x,y=y, width=width, height=height)

			tmplist.append(dd)
		return tmplist

	# @classmethod
	def genjsfl(self, modname, jsflpath):
		self.lindex = 0
		self.pindex = 1
		xmlname = modname+'.xml'
		modname = genPath(jsflpath,modname+'.jsfl')
		text = "//auto generated by python\n"
		text += "var file = fl.configURI + 'KPJSFL/CreateScript.jsfl';\n"
		text += "fl.runScript(file);\n"
		text += "var config_path = get_current_path()+'%s';\n"
		text += "create_doc_path(config_path)\nfl.quit()"

		with open(modname, 'w') as fl:
			fl.write(text % xmlname)

	@classmethod
	def genroot(self, modname):   #modname = commando ...
		rootname = modname+'.fla'
		self.root = et.Element('root',{'doc_name': rootname})

	@classmethod
	def witem(self,types='movie', iname='mc', lname='AnimationClip'):
		self.xitem = et.SubElement(self.root, types, {'item_name':iname, 'link_name': lname})
	
	@classmethod
	def savexml(self,fname):
		root = indent(self.root)
		et.ElementTree(root).write(fname)

	@classmethod
	def wbody(self, pdata, dirname, replace):
		pdata.wlabel(dirname, replace, self.xitem)
		pdata.wpics(dirname, replace, self.xitem)
		if pdata.backpngs:
			pdata.wbackground(self.xitem)

