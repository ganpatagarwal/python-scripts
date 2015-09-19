def foo(a, b, de, ce):
	print a, b, de, ce
lst = [0,1]
dct = {'ce':3, 'de':2}
foo(*lst, **dct) 