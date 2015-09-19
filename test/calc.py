import urllib

#name = raw_input('>')
#url = 'http://finance.yahoo.com/q?s={}'.format(name)
url = 'http://google.co.in'
r = urllib.urlopen(url)
print r.read()
#soup = BeautifulSoup(r.text)
#data = soup.find('span', attrs={'id':'yfs_l84_'.format(name)})
#print data.text
