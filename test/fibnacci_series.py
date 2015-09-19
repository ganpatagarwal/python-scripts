def fibonacci(maxi):
    alist = []
    for i in range(0, maxi+1):
       if i==0:
           alist.append(i)
       if i==1 or i==-1:
           b = alist[i-1] + (i)
           alist.append(b)
       else:
           if i>1 or i<-1:
               c = alist[i-1] + alist[i-2]
               alist.append(c)
    print alist       

fibonacci(3)