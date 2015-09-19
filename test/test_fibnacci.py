# function version
def fibon(n):
    a = 0
    b = 1
    result = []
    for i in xrange(n):
        result.append(a)
        a, b = b, a + b
    return result
    
print fibon(3)
print "#"*20
def fibon_generator(n):
    a = 0
    b = 1
    for i in xrange(n):
        yield a
        a, b = b, a + b

for x in fibon_generator(3):
	print x
	
print "-"*20
a = fibon_generator(3)
print a.next()
print a.next()
print a.next()
#print a.next()