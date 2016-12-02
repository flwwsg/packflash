'''bspdata.py'''
from code.packdata import *

class BSPdata(PackData):
	def __init__(self, modpath):
		PackData.__init__(self, modpath)

	# #pngxy like pngxy['1_2'] [{'xname':'xx', 'xpath':'1_idle','x':x, 'y':y}]
	def wpics(self, dirname, replace, xitem):
		layer = et.SubElement(xitem,'layer',{'name':'pics'})

		backpngs =list()
		if dirname in replace.keys():
			dirname = replace[dirname]
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
				et.SubElement(layer, 'frame', {'quality':PICQUALITY, 'x':str(x), 'y':str(y), 
					'source_path':path, 
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

	def getitems(self, ttxml,replace):
		tmp = scanFile(ttxml)
		xmlpath = list()
		for i in tmp:
			if i[-3:] == 'xml':
				ibn = baseName(i)
				xmlpath.append(i)

		pngxy = dict()
		self.subdir.extend(sorted(replace.keys()))

		for dirname in self.subdir:
			if dirname in replace.keys():
				newdirname = replace[dirname]
			else:
				newdirname = dirname
			# print(newdirname, dirname)
			pngxy[dirname] = BSPdata.getxy(xmlpath)
		self.pngxy = pngxy

	@classmethod
	def getxy(self, paths):
		tmplist = list()
		for path in paths:
			ttxml = et.parse(path)
			root = ttxml.getroot()

			tmp = root.get('imagePath')
			status = tmp[:-4]
			for subtt in root:
				pngpath = subtt.get('name')
				xpath, xname = status, pngpath

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