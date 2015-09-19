import urllib
import os,sys

testfile=urllib.URLopener()
#testfile.retrieve("http://randomsite.com/file.gz","file.gz")

cur_dir = os.getcwd()
file_list = os.listdir(cur_dir)

for i in file_list:print i