import os as sys1
import sys as sys2
#sys.path.append('C:\\scripts\\test\\try')
#import try.py

#print " Printing the value"

a='os'
b='sys'

def find(mod):
	if mod=='os':
		print "printing OS"
		print dir(sys1)
	elif mod=='sys':
		print "printing sys"
		print dir(sys2)

find(b)
