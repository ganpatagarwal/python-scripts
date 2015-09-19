def triangle_triplets_new(alist):
	for i in xrange(len(alist)-1):
		for j in range(i+1,len(alist)-1):
			k = j+1
			while(k<len(alist)):
				blist = []
				blist.append(alist[i])
				blist.append(alist[j])
				blist.append(alist[k])
				#print blist
				print sorted(blist)
				del blist
				k+=1
		
		


#find_largest([2,6,1])
something = [8,9,7,11,15,20]
#triangle_triplets(something)
triangle_triplets_new(something)