@echo off

rmdir /S /Q %TMP_DIR%
cls

:checkJavaInstallation
echo %date%:%time% - DEBUG : Checking for existing Java Installation >>%LOG_FILE%
java -version
if %ERRORLEVEL% equ 9009 goto installJava
java -version 2>&1 | findstr /i "version" > %TEMP_FILE%
set /p CUR_JAVA_VER= <%TEMP_FILE%
set CUR_JAVA_VER=%CUR_JAVA_VER:*"=%
set CUR_JAVA_VER=%CUR_JAVA_VER:"=%
echo %CUR_JAVA_VER% | findstr "%REQ_JAVA_VER%"
if %ERRORLEVEL% equ 0 (
	cls
	echo Required JDK is already installed
	echo %date%:%time% - DEBUG : Required JDK is already installed >>%LOG_FILE%
	pause
	goto checkPath )

if %ERRORLEVEL% neq 0 (
	echo Java version "jdk%REQ_JAVA_VER%" not found in the system
	echo Current Java version "jdk%CUR_JAVA_VER%"
	goto installJava)

:checkPath
set REQ_JAVA_PATH=C:\Program Files\Java\jdk%CUR_JAVA_VER%
if "%REQ_JAVA_PATH%"=="%JAVA_HOME%" (
	goto installJCE
	) else (
		goto setJavaPath)

:installJava
cls
echo Installation for required JDK will start.
pause
jdk-7u65-windows-x64.exe
echo %date%:%time% - DEBUG : Required JDK installation complete >>%LOG_FILE%
echo Required JDK installation complete
pause

:setJavaPath
echo Setting JAVA_HOME path
echo %date%:%time% - INFO : Setting JAVA_HOME path >>%LOG_FILE%
setx JAVA_HOME "%REQ_JAVA_PATH%"

:installJCE
echo Installing JCE
echo %date%:%time% - INFO : Installing JCE >>%LOG_FILE%
chdir %DOWNLOAD_DIR%
7zG e UnlimitedJCEPolicyJDK7.zip -o%TMP_DIR%
copy /Y "%TMP_DIR%\US_export_policy.jar" "%REQ_JAVA_PATH%\jre\lib\security"
copy /Y "%TMP_DIR%\local_policy.jar" "%REQ_JAVA_PATH%\jre\lib\security"

:end
echo %date%:%time% - DEBUG : END of JDK installation >>%LOG_FILE%
rmdir /S /Q %TMP_DIR%
exit

