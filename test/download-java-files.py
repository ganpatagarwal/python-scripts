from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep   
import os
import sys
reload(sys)
sys.setdefaultencoding("utf8")

download_location='C:\scripts\EHAC-Automation\Downloaded-Files'
download_location = download_location.replace('\\','\\\\')

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
	while(part_filename):
		file_list = os.listdir(download_location)
		if part_filename in file_list:
			sleep(10)
			continue
		else:
			part_filename = ''

URL1='http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html'
URL2='http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html'
URL3='https://db.apache.org/derby/derby_downloads.html'
URL4='http://jbossas.jboss.org/downloads/'
URL5='http://jbossweb.jboss.org/downloads/jboss-native-2-0-10.html'

# Firefox driver
driver1 = get_firefox_driver()

#go to URL1
driver1.get(URL1)
driver1.maximize_window()

ele_list = driver1.find_elements_by_tag_name('H3')

ver=''
for e in ele_list:
	att = e.get_attribute('textContent').strip()
	if att.find('Java SE Development Kit')>=0:
		ver=att.strip('Java SE Development Kit')
		break

agg_link1 = driver1.find_element_by_name("agreementjdk-%s-oth-JPR"%ver)
agg_link1.click()

download_link1 = driver1.find_element_by_name("jdk-%s-oth-JPRXXXjdk-%s-windows-x64.exe"%(ver,ver))
download_link1.click()
download_filename1 = 'jdk-%s-windows-x64.exe'%ver
download_link1.send_keys(Keys.CONTROL + 'j')
wait_till_download_completes(download_location,download_filename1)

# Close the browser!
driver1.quit()

# Firefox driver
driver2 = get_firefox_driver()

#go to URL2
driver2.get(URL2)
driver2.maximize_window()

agg_link2= driver2.find_element_by_name("agreementjce-7-oth-JPR")
agg_link2.click()

download_link2 = driver2.find_element_by_name("jce-7-oth-JPRXXXUnlimitedJCEPolicyJDK7.zip")
download_link2.click()
download_filename2 = 'UnlimitedJCEPolicyJDK7.zip'
download_link2.send_keys(Keys.CONTROL + 'j')
wait_till_download_completes(download_location,download_filename2)

# Close the browser!
driver2.quit()

# Firefox driver
driver3 = get_firefox_driver()

#go to URL3
driver3.get(URL3)
driver3.maximize_window()

ele_list = driver3.find_elements_by_tag_name('a')

att_dict={}
for e in ele_list:
	att = e.get_attribute('textContent').strip()
	if att.find('10.8.')>=0:
		att_dict[att]=e
key_list=att_dict.keys()
key_list.sort()
derby_latest_ver=key_list[len(key_list)-1]
download_link_temp = att_dict[derby_latest_ver]
download_link_temp.click()

download_link3=''
download_filename3='db-derby-%s-lib.zip'%derby_latest_ver
ele_list = driver3.find_elements_by_tag_name('A')

for e in ele_list:
	att = e.get_attribute('textContent').strip()
	if att == download_filename3:
		download_link3=e
if download_link3:
	download_link3.click()
	download_link3.send_keys(Keys.CONTROL + 'j')
	wait_till_download_completes(download_location,download_filename3)

# Close the browser!
driver3.quit()


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


# Firefox driver
driver5 = get_firefox_driver()

#go to URL5
driver5.get(URL5)
driver5.maximize_window()

download_filename5='jboss-native-2.0.10-windows-x64-ssl.zip'
download_link5=''
ele_list = driver5.find_elements_by_class_name('td-download')

for e in ele_list:
	att = e.get_attribute('href').strip()
	if att.find(download_filename5)>=0:
		download_link5=e
if download_link5:
	download_link5.click()
	continue_link = ''
	ele_list = driver5.find_elements_by_tag_name('A')
	for e in ele_list:
		att = e.get_attribute('textContent').strip()
		if att == 'Continue Download':
			continue_link = e
			continue_link.click()
			break
	download_link5.send_keys(Keys.CONTROL + 'j')
	wait_till_download_completes(download_location,download_filename5)

# Close the browser!
driver5.quit()
