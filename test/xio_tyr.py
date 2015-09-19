import urllib
import urllib2
import base64
import json
 
url = "https://10.110.42.220/api/json/types/initiator-groups/"
authKey = base64.b64encode("admin:Xtrem10")
print authKey
headers = {"Content-Type":"application/json", "Authorization":"Basic " + authKey}
#data = { "ig-id" : "osc_test1"}
data = {"ig-name":"gan_test_ig", "parent-folder-id":'/'}
#edata = urllib.urlencode(data)
jdata=json.dumps(data)
request = urllib2.Request(url, data = jdata, headers =headers )
# post form data
#request.add_data(urllib.urlencode(data))
#for key,value in headers.items():
#	request.add_header(key,value)
#print request.get_method()
response = urllib2.urlopen(request)
#print response.info().headers
print response.read()
