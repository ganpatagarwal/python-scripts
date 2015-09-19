@echo off

:setLocalVariables
set APP_DIR=%cd%
set TMP_DIR=%APP_DIR%\tmp
set DERBY_DIR=C:\derby-jar
set JBOSS_DIR=C:\jboss
set LOG_FILE=Install-Log.log
set JBOSS_SERVICE=JBAS50SVC
set JBOSS_SERVICE1=JBOSS
set REQ_JAVA_PATH=C:\Program Files\Java\jdk1.7.0
set REQ_JAVA_VER=1.7
set TEMP_FILE=tmpFile
set OUT_FILE=OutputFile
set DOWNLOAD_DIR=%APP_DIR%\Downloaded-Files

echo ==============================================================>%LOG_FILE%

:check
setenv -e
if %ERRORLEVEL% neq 0 (
	cls
	echo %date%:%time% - ERROR : setenv application is not installed >>%LOG_FILE%
	goto end)
cls
7z
if %ERRORLEVEL% neq 0 (
	cls
	echo %date%:%time% - ERROR : 7z application is not installed >>%LOG_FILE%
	goto end)
cls
python -h
if %ERRORLEVEL% equ 9009 (
	cls
	echo %date%:%time% - ERROR : Python is not installed >>%LOG_FILE%
	goto end)
cls

:checkAndInstallPythonTools
easy_install selenium
if %ERRORLEVEL% equ 9009 (
	cls
	echo %date%:%time% - INFO : Installing easy_install tool ..... >>%LOG_FILE%
	echo Installing easy_install - A python tool ......
	python ez_setup.py
	echo %date%:%time% - DEBUG : Installation Complete >>%LOG_FILE%
	echo easy_install Installation Complete
	goto checkAndInstallPythonTools )
cls
echo Selenium installtion complete
echo %date%:%time% - DEBUG : Selenium installtion complete >>%LOG_FILE%
pause
cls

:startInstallation
python download_files.py %DOWNLOAD_DIR%
::python pass_vals.py %DOWNLOAD_DIR%
if %ERRORLEVEL% neq 0 (
	echo %date%:%time% - ERROR : Error while downloading files >>%LOG_FILE%
	echo %date%:%time% - INFO : Installation Failed >>%LOG_FILE%
	echo Error While downloading files
	pause
	goto end )
echo %date%:%time% - INFO : Installation Complete >>%LOG_FILE%

:createReport
cls
echo OUTPUT FILE : %APP_DIR%\%OUT_FILE% >>%LOG_FILE%
echo DERBY_DIR=C:\derby-jar >%OUT_FILE%
echo JBOSS_DIR=C:\jboss >>%OUT_FILE%
echo LOG_FILE - %APP_DIR%\Install-Log.log >>%OUT_FILE%
echo.
type %OUT_FILE%
echo.
echo.
echo Please find the necessary details in the file : %APP_DIR%\%OUT_FILE%
echo.
echo.

:end
echo.
echo ********** Install Log ************************
echo.
type %LOG_FILE%
pause