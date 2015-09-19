a = "heblloza"
l1= []
l2= []

for i in range(0,len(a)):
	l1.append(a[i])
	
while(l1):
	print l1
	min_val = l1[0]
	for j in range(0,len(l1)):		
		if l1[j] < min_val:
			min_val = l1[j]
	print min_val
	l2.append(min_val)
	l1.remove(min_val)
	
print ''.join(l2)

def sorastring(strr):
	strr = [strr]
	print 'first',strr
	dev = []
	d=''
	for i in range(0, len(strr)):
		print i
		print strr[i]
		if strr[i]<strr[i+1]:
			print strr[i]
			strr[i], strr[i+1] = strr[i+1], strr[i]
	print 'second',strr

sorastring("banana")