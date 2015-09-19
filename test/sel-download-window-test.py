from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import sys
reload(sys)
sys.setdefaultencoding("utf8")


download_location='C:\\Users\\agarwg1\\Downloads'
URL1='http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html'
URL2='http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html'
URL3='https://db.apache.org/derby/derby_downloads.html'
URL4='http://jbossas.jboss.org/downloads/'
URL5='http://jbossweb.jboss.org/downloads/jboss-native-2-0-10.html'


def get_firefox_driver():
	#Create a customized FireFox profile
	fp = webdriver.FirefoxProfile()

	fp.set_preference("browser.download.folderList",2)		 	
	fp.set_preference("browser.download.manager.showWhenStarting",False)
	fp.set_preference("browser.download.dir",download_location)
	fp.set_preference("browser.helperApps.neverAsk.openFile", "application/zip,application/octet-stream")
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/zip,application/octet-stream")
	fp.set_preference("browser.download.manager.scanWhenDone",False)
	fp.set_preference("browser.download.manager.showAlertOnComplete",True)
	fp.set_preference("browser.download.manager.useWindow",False)
	fp.set_preference("browser.helperApps.alwaysAsk.force",False)
	
	return webdriver.Firefox(firefox_profile=fp)

def wait_till_download_completes(download_location,filename):
	part_filename = filename+'.part'
	sleep(2)
	#print part_filename
	while(part_filename):
		file_list = os.listdir(download_location)
		print file_list
		if part_filename in file_list:
			print 'hello'
			sleep(10)
			continue
		else:
			part_filename = ''
	#return
			
# Firefox driver
driver4 = get_firefox_driver()

#go to URL4
driver4.get(URL4)
driver4.maximize_window()

download_filename4='jboss-as-7.1.1.Final.zip'
download_link4=''
ele_list = driver4.find_elements_by_class_name('td-download')

for e in ele_list:
	att = e.get_attribute('href').strip()
	if att.find(download_filename4)>=0:
		download_link4=e
if download_link4:
	download_link4.click()
	continue_link = ''
	ele_list = driver4.find_elements_by_tag_name('A')
	for e in ele_list:
		att = e.get_attribute('textContent').strip()
		if att == 'Continue Download':
			continue_link = e
			continue_link.click()
			break
	download_link4.send_keys(Keys.CONTROL + 'j')
	wait_till_download_completes(download_location,download_filename4)

# Close the browser!
driver4.quit()