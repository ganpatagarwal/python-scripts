import os
import sys

print "In python program"

download_filename=sys.argv[1]
download_filename = download_filename.replace('\\','\\\\')
print download_filename

download_filename1 = 'jdk-7u67-windows-x64.exe'
download_filename2 = 'UnlimitedJCEPolicyJDK7.zip'
download_filename3='db-derby-10.8.3.0-lib.zip'
download_filename4='jboss-as-7.1.1.Final.zip'
download_filename5='jboss-native-2.0.10-windows-x64-ssl.zip'

os.system("Start-Install.bat %s %s %s %s %s"%(download_filename1,
								download_filename2,
								download_filename3,
								download_filename4,
								download_filename5))
