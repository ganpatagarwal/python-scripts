class Find:
	def large_number(self, num):
		num = map(str,num)
		print num
		num.sort(cmp=self.compare,reverse=True)
		print num
		return str(int("".join(num)))
	def compare(self, a, b):
		if a+b > b+a:
			return 1
		elif a+b < b+a:
			return -1
		else:
			return 0

find = Find()
print find.large_number([8,3, 30, 34, 5,80, 9])