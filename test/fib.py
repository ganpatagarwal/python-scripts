"""
Fibnacci Series
"""

def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

num = int(raw_input("Enter the number of terms : "))
print map(fib, range(num+1))