'''misc.py'''

import threading 
DEBUG = True

FLOCK = threading.Lock()
def genThread(func, *args):
	newthread = threading.Thread(target=func, args=(*args,)).start()
	return newthread
