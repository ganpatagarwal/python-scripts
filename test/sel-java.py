# To install the Python client library:
# pip install -U selenium
 
# Import the Selenium 2 namespace (aka "webdriver")
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep   
import os
 
# iPhone
#driver = webdriver.Remote(browser_name="iphone", command_executor='http://172.24.101.36:3001/hub')
 
# Android
#driver = webdriver.Remote(browser_name="android", command_executor='http://127.0.0.1:8080/hub')
 
# Google Chrome 
#driver = webdriver.Chrome()
 

download_location='C:\\Users\\agarwg1\\Downloads'

fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList",2)		 	
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir",download_location)
fp.set_preference("browser.helperApps.neverAsk.openFile", "application/zip")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/zip")
fp.set_preference("browser.download.manager.scanWhenDone",False)
fp.set_preference("browser.download.manager.showAlertOnComplete",True)
fp.set_preference("browser.download.manager.useWindow",False)
fp.set_preference("browser.helperApps.alwaysAsk.force",False)


# Firefox 
driver = webdriver.Firefox(firefox_profile=fp)

#go to URL
driver.get('http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html')
 
# Select the Python language option
#python_link = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
#python_link = driver.find_elements_by_xpath("html/body/div/center/table/tbody/tr/td[1]/div/form/table/tbody/tr[2]/td[1]/nobr[10]/label/span")[0]
#python_link.click()
 
# Enter some text!
#text_area = driver.find_element_by_id('textarea')
#text_area.send_keys("print 'Hello,' + ' World!'")
 
# Submit the form!
#submit_button = driver.find_element_by_name('submit')
#submit_button.click()
 
# Make this an actual test. Isn't Python beautiful?
#assert "Hello, World!" in driver.get_page_source()
 
#agg_link = driver.find_elements_by_xpath("html/body/div[4]/div[3]/div[2]/div[1]/div[3]/div/table/tbody/tr[2]/th/div/div[1]/form/input[1]")


#print driver.current_url  #to get the current url


agg_link = driver.find_element_by_name("agreementjce-7-oth-JPR")
agg_link.click()

download_link = driver.find_element_by_name("jce-7-oth-JPRXXXUnlimitedJCEPolicyJDK7.zip")

#print download_link.get_attribute("href") #to get the href of an element
download_link.click()

#going to sleep to enable the file download
sleep(5)

# Close the browser!
driver.quit()

dowanload_list = os.listdir(download_location)
for file in dowanload_list : print file