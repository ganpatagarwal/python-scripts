import xmlrpclib

user = "esi\Administrator"
password = "Password!"
ip_add = '10.31.219.172'
port = '8237'

uri = "http://%s:%s"%(ip_add,port)

print uri

server = xmlrpclib.ServerProxy(uri,verbose=True)

print server.get_keyword_names()