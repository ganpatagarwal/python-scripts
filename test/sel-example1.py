import os

from selenium import webdriver

fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

browser = webdriver.Firefox(firefox_profile=fp)
browser.get("http://www.oracle.com/technetwork/java/javase/downloads/jce-7-download-432124.html")
browser.find_element_by_name("agreementjce-7-oth-JPR").click()
browser.find_element_by_name("jce-7-oth-JPRXXXUnlimitedJCEPolicyJDK7.zip").click()