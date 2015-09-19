import os

def utopian_tree(val,cycles):
	if cycles == 0: return val
	else:
		for i in range (1,cycles+1):
			if i%2 != 0:
				val = val * 2
			else:
				val = val +1
		return val


N = raw_input("enter total number of trees :")
val = raw_input("enter %s values separated by space : "%N )
val_list = val.split()
val_list = val_list[0:int(N)]
val_list = map(int,val_list)
#print val_list

#val_list = [5,4,4,0,2,8]

	
while(val_list):
	
	m = min(val_list)
	for i in range(0,len(val_list)):
		val_list[i] -= m
	print len(val_list)
	
	while 0 in val_list:
		val_list.remove(0)
	
	
	
	
	
	