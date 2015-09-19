#EMC Copyright

"""This file uses selenium to download required files"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import sys
reload(sys)

DOWNLOAD_LOCATION = sys.argv[1]
DOWNLOAD_LOCATION = DOWNLOAD_LOCATION.replace('\\', '\\\\')
if os.path.exists(DOWNLOAD_LOCATION):
    os.system("rmdir /S /Q %s"%DOWNLOAD_LOCATION)

def get_firefox_driver():
    """This function returns a new object for firefox driver"""
    #Create a customized FireFox profile
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference(\
        "browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.download.dir", DOWNLOAD_LOCATION)
    firefox_profile.set_preference("browser.helperApps.neverAsk.openFile", \
        "application/zip,application/octet-stream")
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", \
        "application/zip,application/octet-stream")
    firefox_profile.set_preference(\
        "browser.download.manager.scanWhenDone", False)
    firefox_profile.set_preference(\
        "browser.download.manager.showAlertOnComplete", True)
    firefox_profile.set_preference("browser.download.manager.useWindow", False)
    firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    return webdriver.Firefox(firefox_profile=firefox_profile)

def wait_till_download_completes(driver, filename, \
                        download_dir=DOWNLOAD_LOCATION):
    """Wait till the download of a file is complete"""
    part_filename = filename+'.part'
    sleep(2)
    while part_filename:
        file_list = os.listdir(download_dir)
        if part_filename in file_list:
            sleep(10)
            continue
        else:
            part_filename = ''
    driver.quit()

URL1 = 'http://www.oracle.com/technetwork/\
java/javase/downloads/jdk7-downloads-1880260.html'
URL2 = 'http://www.oracle.com/technetwork/java/\
javase/downloads/jce-7-download-432124.html'
URL3 = 'https://db.apache.org/derby/derby_downloads.html'
URL4 = 'http://jbossas.jboss.org/downloads/'
URL5 = 'http://jbossweb.jboss.org/downloads/jboss-native-2-0-10.html'

try:
    # Firefox driver
    DRIVER1 = get_firefox_driver()

    #go to URL1
    DRIVER1.get(URL1)
    DRIVER1.maximize_window()

    ELE_LIST = DRIVER1.find_elements_by_tag_name('H3')

    VER = ''
    for e in ELE_LIST:
        ATT = e.get_attribute('textContent').strip()
        if ATT.find('Java SE Development Kit') >= 0:
            VER = ATT.strip('Java SE Development Kit')
            break

    AGG_LINK1 = DRIVER1.find_element_by_name("agreementjdk-%s-oth-JPR"%VER)
    AGG_LINK1.click()

    DOWNLOAD_LINK1 = DRIVER1.find_element_by_name(\
                        "jdk-%s-oth-JPRXXXjdk-%s-windows-x64.exe"%(VER, VER))
    DOWNLOAD_LINK1.click()
    DOWNLOAD_FILENAME1 = 'jdk-%s-windows-x64.exe'%VER
    DOWNLOAD_LINK1.send_keys(Keys.CONTROL + 'j')
    wait_till_download_completes(DRIVER1, DOWNLOAD_FILENAME1)
except Exception:
    DRIVER1.quit()
    print "Error while downloading file fom URL : \n%s"%URL1
    exit(1)

try:
    # Firefox driver
    DRIVER2 = get_firefox_driver()

    #go to URL2
    DRIVER2.get(URL2)
    DRIVER2.maximize_window()

    AGG_LINK2 = DRIVER2.find_element_by_name("agreementjce-7-oth-JPR")
    AGG_LINK2.click()

    DOWNLOAD_LINK2 = DRIVER2.find_element_by_name(\
                          "jce-7-oth-JPRXXXUnlimitedJCEPolicyJDK7.zip")
    DOWNLOAD_LINK2.click()
    DOWNLOAD_FILENAME2 = 'UnlimitedJCEPolicyJDK7.zip'
    DOWNLOAD_LINK2.send_keys(Keys.CONTROL + 'j')
    wait_till_download_completes(DRIVER2, DOWNLOAD_FILENAME2)
except Exception:
    DRIVER2.quit()
    print "Error while downloading file fom URL : \n%s"%URL2
    exit(1)

try:
    # Firefox driver
    DRIVER3 = get_firefox_driver()

    #go to URL3
    DRIVER3.get(URL3)
    DRIVER3.maximize_window()

    ELE_LIST = DRIVER3.find_elements_by_tag_name('a')

    ATT_DICT = {}
    for e in ELE_LIST:
        ATT = e.get_attribute('textContent').strip()
        if ATT.find('10.8.') >= 0:
            ATT_DICT[ATT] = e
    KEY_LIST = ATT_DICT.keys()
    KEY_LIST.sort()
    DERBY_LATEST_VER = KEY_LIST[len(KEY_LIST)-1]
    DOWNLOAD_LINK_TEMP = ATT_DICT[DERBY_LATEST_VER]
    DOWNLOAD_LINK_TEMP.click()

    DOWNLOAD_FILENAME3 = 'db-derby-%s-lib.zip'%DERBY_LATEST_VER
    ELE_LIST = DRIVER3.find_elements_by_tag_name('A')

    for e in ELE_LIST:
        ATT = e.get_attribute('textContent').strip()
        if ATT == DOWNLOAD_FILENAME3:
            DOWNLOAD_LINK3 = e
    if DOWNLOAD_LINK3:
        DOWNLOAD_LINK3.click()
        DOWNLOAD_LINK3.send_keys(Keys.CONTROL + 'j')
        wait_till_download_completes(DRIVER3, DOWNLOAD_FILENAME3)
except Exception:
    DRIVER3.quit()
    print "Error while downloading file fom URL : \n%s"%URL3
    exit(1)

try:
    # Firefox driver
    DRIVER4 = get_firefox_driver()

    #go to URL4
    DRIVER4.get(URL4)
    DRIVER4.maximize_window()

    DOWNLOAD_FILENAME4 = 'jboss-as-7.1.1.Final.zip'
    ELE_LIST = DRIVER4.find_elements_by_class_name('td-download')

    for e in ELE_LIST:
        ATT = e.get_attribute('href').strip()
        if ATT.find(DOWNLOAD_FILENAME4) >= 0:
            DOWNLOAD_LINK4 = e
    if DOWNLOAD_LINK4:
        DOWNLOAD_LINK4.click()
        CONTINUE_LINK = ''
        ELE_LIST = DRIVER4.find_elements_by_tag_name('A')
        for e in ELE_LIST:
            ATT = e.get_attribute('textContent').strip()
            if ATT == 'Continue Download':
                CONTINUE_LINK = e
                CONTINUE_LINK.click()
                break
        DOWNLOAD_LINK4.send_keys(Keys.CONTROL + 'j')
        wait_till_download_completes(DOWNLOAD_LOCATION, DOWNLOAD_FILENAME4)
except Exception:
    DRIVER4.quit()
    print "Error while downloading file fom URL : \n%s"%URL4
    exit(1)

try:
    # Firefox driver
    DRIVER5 = get_firefox_driver()

    #go to URL5
    DRIVER5.get(URL5)
    DRIVER5.maximize_window()

    DOWNLOAD_FILENAME5 = 'jboss-native-2.0.10-windows-x64-ssl.zip'
    ELE_LIST = DRIVER5.find_elements_by_class_name('td-download')

    for e in ELE_LIST:
        ATT = e.get_attribute('href').strip()
        if ATT.find(DOWNLOAD_FILENAME5) >= 0:
            DOWNLOAD_LINK5 = e
    if DOWNLOAD_LINK5:
        DOWNLOAD_LINK5.click()
        CONTINUE_LINK = ''
        ELE_LIST = DRIVER5.find_elements_by_tag_name('A')
        for e in ELE_LIST:
            ATT = e.get_attribute('textContent').strip()
            if ATT == 'Continue Download':
                CONTINUE_LINK = e
                CONTINUE_LINK.click()
                break
        DOWNLOAD_LINK5.send_keys(Keys.CONTROL + 'j')
        wait_till_download_completes(DOWNLOAD_LOCATION, DOWNLOAD_FILENAME5)
except Exception:
    DRIVER5.quit()
    print "Error while downloading file fom URL : \n%s"%URL5
    exit(1)

#calling the batch script to install the above downloaded files
os.system("Start-Install.bat %s %s %s %s %s"%(DOWNLOAD_FILENAME1,\
                                DOWNLOAD_FILENAME2,\
                                DOWNLOAD_FILENAME3,\
                                DOWNLOAD_FILENAME4,\
                                DOWNLOAD_FILENAME5))
