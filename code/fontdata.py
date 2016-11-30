#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from code.packdata import *

class FontData(PackData):
	def __init__(self):
		self.gconfig()

	@classmethod
	def gconfig(self):
		self.item_name = 'YaHei'
		self.font_name = 'Microsoft YaHei'
		self.link_name = 'MyFont'
		self.isfte = 'false'
		self.bold = 'false'
		self.italic = 'false'
		self.embed_ranges = '1|2|3|4|5'

	@classmethod
	def genroot(self, modname):   
		rootname = modname+'.fla'
		self.root = et.Element('root',{'doc_name': rootname})

	@classmethod
	def witem(self, types='font'):
		self.xitem = et.SubElement(self.root, types, {'item_name':self.item_name,'font_name':self.font_name, 'link_name': self.link_name,
										'is_FTE':self.isfte, 'bold':self.bold, 'italic':self.italic,'embed_ranges':self.embed_ranges})

	@classmethod
	def wbody(self, data):
		if isinstance(data, str):
			data = [data]
		for tmp in data:
			self.xitem.append(et.Comment(' --><![CDATA[' + tmp.replace(']]>', ']]]]><![CDATA[>') + ']]><!-- '))