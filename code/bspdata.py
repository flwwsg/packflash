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