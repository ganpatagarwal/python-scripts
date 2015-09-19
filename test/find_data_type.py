
def define_data_type(list1):
	for item in list1:
		try:
			if item.isdigit():print item+" digit" #isdigit function is used to find a digit inside string quotes
			else:print item+" string"
		except:
			data_type = str(type(item))
			#print type(data_type)
			d = data_type.split("'")
			#print d
			print item,d[1]
	
		
list1 = ['a',1,'hello',1.12,'2']
define_data_type(list1)