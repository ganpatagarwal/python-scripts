def sort_n_count_old(given):
	given2 = []
	count = 0
	length = len(given)
	for i in range (0, len(given)):
		for j in range (0, len(given)):
			print given[j]
			if given[i]==given[j]:
				count = count + 1
				

		if given[i] not in given2:
			given2.append(given[i])
			given2.append("count"+ str(count))
		count = 0


	print given2

def sort_n_count(given):
	d = {}
	ctr = 0
	for i in range (0, len(given)):
		keys = d.keys()
		for j in range(0,len(keys)):
			if given[i] == keys[j]:
				ctr +=1
		if ctr == 0:
			count =0
			print given[i] #checking to see the iteration
			for k in range (0, len(given)):
				if given[i]==given[k]:
					count = count + 1
			d[given[i]] = count
		else:
			ctr = 0
		
	print d
	
sort_n_count([1, 2, 1, 4, 1, 1, 2, 3, 2, 4, 1, 4, 3])