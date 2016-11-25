#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from __future__ import print_function
# import animationHelper as helper
# import animaFunc as funcs
import code.packHelper as helper
# import shutil
# from packer import Packer
# from packtools import PackTools
# from soldier import Soldier
# from packdata import PackData
import os 

# replace =dict()
# replace['6_6'] = '2_0'
# replace['7_5'] = '3_1'
# replace['8_4'] = '1_2'

# xmlpath= {'2_0': 'd:\\dev\\packflash\\tmp\\texture\\commando-mobs\\2_0.xml', '3_1': 
# 'd:\\dev\\packflash\\tmp\\texture\\commando-mobs\\3_1.xml', 
# '5_3': 'd:\\dev\\packflash\\tmp\\texture\\commando-mobs\\5_3.xml',
#  '1_2': 'd:\\dev\\packflash\\tmp\\texture\\commando-mobs\\1_2.xml', 
#  '4_7': 'd:\\dev\\packflash\\tmp\\texture\\commando-mobs\\4_7.xml'}

srcdir = 'd:/dev/packflash/src'
dest = 'd:/dev/packflash/tmp/tempsource'
dirs = helper.scanDir(srcdir)
copy2tmpsrc(dirs, dest)