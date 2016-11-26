'''misc.py'''

import threading 
DEBUG = True

FLOCK = threading.Lock()
def genThread(func, *args):
	target = func
	threading.Thread(target=target, args=(*args,)).start()

if __name__ == '__main__':
	func = 'newfunc'
	args = 'a,b,c,d,e'
	genThread(func, 'a','b','c','end')