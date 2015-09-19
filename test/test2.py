import os

def someFun():
	try : x= 1/0
	except: print "divide by zero"
	
try:someFun()
finally : cleanup()

def cleanup():
	print "cleanup"