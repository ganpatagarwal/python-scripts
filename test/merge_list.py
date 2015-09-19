def merge_list(l1,l2):
	for item in l2:
		l1 = l1 + [item]
	return l1
	
l1 = ['1','a',2,3,4]
l2 = [5,6,7,8,9]
print merge_list(l1,l2)

#see these links for perfomance
#http://stackoverflow.com/questions/252703/python-append-vs-extend