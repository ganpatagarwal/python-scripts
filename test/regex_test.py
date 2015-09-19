str = "dFD$#23+++12@#T1234;/.,10"	
i = 0
l = len(str)
sum =0
while (i < l):
	temp = str[i]
	if temp.isdigit():
		is_digit = True
		num = temp
		j = i+1
		while (j <l and is_digit):
			next = str[j]
			if next.isdigit():
				num = num+next
				j = j+1
			else:
				is_digit = False
		#print num
		sum += int(num)
		i = j+1
	else:
		i+=1
	
print "Sum is : ",sum