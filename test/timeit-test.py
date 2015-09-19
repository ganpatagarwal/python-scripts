import timeit

start = timeit.default_timer()

v =10
for i in range(1,10):
	v = v*i
	
print v

stop = timeit.default_timer()

print stop - start 