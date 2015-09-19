l1 = ['1', '2', {'a' : 'gans', 'b' : ['3', '4', {'d':'world', 'e' : ['4','5',{'f':'new'}]}]}]
l2 = {'i' : ['1', '2', {'a' : 'gans', 'b' : ['3', '4', {'d':'world', 'e' : ['4','5',{'f':'new'}]}]}], 'j' : 'hell'}

def update_data(data, update_dict):
	if (str(type(data)) == "<type 'list'>"):
		parse_list(data, update_dict)
	elif (str(type(data)) == "<type 'dict'>"):
		parse_dict(data, update_dict)
	return data
		
	
def parse_list(data, update_dict):
	for item in data:
		if (str(type(item)) == "<type 'list'>"):parse_list(item, update_dict)
		if (str(type(item)) == "<type 'dict'>"):parse_dict(item, update_dict)

def parse_dict(data, update_dict):
	for k,v in data.iteritems():
		if (str(type(v)) == "<type 'list'>"):parse_list(v, update_dict)
		if (str(type(v)) == "<type 'dict'>"):parse_dict(v, update_dict)
		for k1,v1 in update_dict.iteritems():
			if k1 == k:
				data[k] = v1
				break
		
#print update_data(l2,{'a':'hello', 'd':'world1', 'f' : {'z':'a'}})

data = [{u'or': [u'all_sender_recipient_access_list', u'SUBSTR', u'Garry.Jorge@PIVOTAL.COM', u'all_sender_recipient_access_list2', u'SUBSTR', u'Aioria@PIVOTAL.COM']}, u'date', u'>=', u'2014-12-02T00:00:00Z', u'date', u'<=', u'2015-07-02T00:00:00Z']
def create_query(data):
	for item in data:
		print item
		
create_query(data)
	
		

		