def wrapper(func, args):
	arg = ', '.join(args)
	func(arg.split())

def func1(x):
    print(x)

def func2(x, y, z):
    return x+y+z

x=1
y=2
z=3
wrapper(func1, [x])
wrapper(func2, [x, y, z])