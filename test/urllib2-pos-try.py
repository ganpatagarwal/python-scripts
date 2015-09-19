import urllib2
import urllib
import base64

# make a string with the request type in it:
method = "POST"
# create a handler. you can specify different handlers here (file uploads etc)
# but we go for the default
handler = urllib2.HTTPHandler()
# create an openerdirector instance
opener = urllib2.build_opener(handler)
# build a request
url = "http://10.110.42.220/api/json/types/initiator-groups/"
data = {"ig-name":"gan_test_ig", "parent-folder-id":'/'}
data = urllib.urlencode(data)
authKey = base64.b64encode("admin:Xtrem10")
request = urllib2.Request(url, data=data )
# add any other information you want
request.add_header("Content-Type",'application/json')
request.add_header("Authorization","Basic " + authKey)
# overload the get method function with a small anonymous function...
request.get_method = lambda: method
# try it; don't forget to catch the result
try:
    connection = opener.open(request)
except urllib2.HTTPError,e:
    connection = e

# check. Substitute with appropriate HTTP code.
if connection.code == 200:
    data = connection.read()
    print data
else:
    print "ERROR"