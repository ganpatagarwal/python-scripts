"""Script to edit the service.bat file"""

import os
import sys

JBOSS_BIN_DIR = sys.argv[1]
JBOSS_BIN_DIR = JBOSS_BIN_DIR.replace('\\', '\\\\')
SOURCE_FILE = 'service.bat'
FILE_LIST = os.listdir(JBOSS_BIN_DIR)

if SOURCE_FILE not in FILE_LIST:
    print "Required file - %s not found"%SOURCE_FILE
    exit(1)

#Open the SOURCE and TARGET files
os.chdir(JBOSS_BIN_DIR)
TARGET_FILE = 'service-new.bat'
SOURCE = open(SOURCE_FILE, 'r')
TARGET = open(TARGET_FILE, 'w+')

#Defining the search texts
SEARCH_TEXT_1 = 'run.bat'
SEARCH_TEXT_2 = 'call shutdown -S < .s.lock >> shutdown.log 2>&1'
SEARCH_TEXT_3 = 'set JAVA_OPTS=-Xrs'
SEARCH_TEXT_4 = 'JBoss Application Server 5.0.0'
SEARCH_TEXT_5 = 'JBoss Application Server 5.0'

#Defining the replace texts
REPLACE_TEXT_1 = 'standalone.bat'
REPLACE_TEXT_2 = 'jboss-cli.bat --connect \
    command=:shutdown >> shutdown.log 2>&1'
REPLACE_TEXT_3 = 'REM set JAVA_OPTS=-Xrs'
REPLACE_TEXT_4 = 'JBoss Application Server 7.1.1'
REPLACE_TEXT_5 = 'JBoss Application Server 7.1'

#search for the text and replace in each line of the TARGET file
for line in SOURCE:
    line = line.replace(SEARCH_TEXT_1, REPLACE_TEXT_1)
    line = line.replace(SEARCH_TEXT_2, REPLACE_TEXT_2)
    line = line.replace(SEARCH_TEXT_3, REPLACE_TEXT_3)
    line = line.replace(SEARCH_TEXT_4, REPLACE_TEXT_4)
    line = line.replace(SEARCH_TEXT_5, REPLACE_TEXT_5)
    TARGET.write(line)

#close the SOURCE and TARGET files
SOURCE.close()
TARGET.close()

#rename the files
TMP_FILE = 'service.bat.bak'

os.rename(SOURCE_FILE, TMP_FILE)
os.rename(TARGET_FILE, SOURCE_FILE)
os.remove(TMP_FILE)