import math

def factors(n):
    results = set()
    for i in xrange(1,int(math.sqrt(n))+1):
        if n%i == 0:
            results.add(i)
            results.add(n/i)
    return results
    
print factors(64)

def rev(name):
	l = len(name)
	new_name = ''
	while l > 0:
		l = l-1
		print name[l]
		new_name += name[l]
	return new_name

name = 'aabba'
if name == rev(name):
	print "palindrome"
		