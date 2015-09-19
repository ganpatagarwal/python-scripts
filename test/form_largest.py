#l = [100,1,2,2,6,67,3,4,30,34,42,45,5,5,20,9]
l = [3, 30, 34, 5, 9]
#sorting the initial list
l.sort()
print l

l2 = []
d= {}

#taking out the first digit from each number 
for item in l:
	tmp = str(item)
	d[tmp[0]] = item
	
keys =  sorted(d.keys())
#print keys

for i in range (len(keys)):
	val = keys[i]
	for item in l:
		tmp = str(item)
		if tmp[0] == str(val):
			l2.append(str(item))
		
print l2
		
#creatng the biggest possible integer
s = ''
i = len(l2) - 1
while(i >=0):
	s += str(l2[i])
	i -= 1
print s
	