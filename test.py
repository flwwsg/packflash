#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''test.py'''
import code.packHelper as helper
import os
# import code.packexp as packexp
from code.packexp import PackExp
from code.soldier import Soldier
from code.cleanprocess import copySVN
from code.packdata import PackData

out = r'd:\dev\packflash\tmp\texture\armor_factory-jz'
tmp = helper.scanFile(out)
xmlpath = dict()
for i in tmp:
	if i[-3:] == 'xml':
		ibn = helper.baseName(i)
		xmlpath[ibn[:-4]]=i

modname = 'armor_factory'
dirname = '1_1'
jsfl = r'D:\dev\packflash\tmp\kpjsfl'
fn = r'D:\dev\packflash\tmp\tempsource\armor_factory-jz'
pdata = PackData(fn)
# print(pdata.subdir, pdata.status)
pngnums =PackData.countPics(fn,pdata.subdir,pdata.status)
# print(pngnums)
pngxy = PackData.getitems(out,pdata.subdir,replace=dict())
# print(pngxy)
pdata.genjsfl(modname,jsfl)
root = PackData.genroot(modname)
titem = PackData.witem(root)
backpng = PackData.wlabel(dirname,pngnums,pdata.status,dict(),titem)
# print(backpng)
backpngs = PackData.wpics(dirname, pngxy,dict(),out+'_cut', titem)
# print(backpngs)
if backpngs:
	PackData.wbackground(backpngs, titem)
PackData.savexml(root,helper.genPath(jsfl,modname+'.xml'))

