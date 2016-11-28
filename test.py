#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''test.py'''

from code.packexp import PackExp
from code.cleanprocess import Cleanprocess
from code.preprocess import Preprocess 

jsfl = r'D:\dev\packflash\tmp\kpjsfl'
fn = r'D:\dev\packflash\finalsource/units/soldiers/gunner_en.swf'
src = 'd:/dev/packflash/src'
try:
	clean = Cleanprocess()
	Cleanprocess.copy2SVN(fn,'soldiers','units','xx#xxy#')
except PackExp as e:
	e.wlog()

# pp = Preprocess()
# pp.renameCN()