import os

dict={}
dict['a']='a'
dict['abb']='a'
dict['b']='a'
dict['c']='a'
dict['ca']='a'

print dict
keys=dict.keys()
keys.sort()
print keys
for k in keys.sort():
	print k