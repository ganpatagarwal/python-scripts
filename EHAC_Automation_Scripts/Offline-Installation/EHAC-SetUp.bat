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

echo ==============================================================>%LOG_FILE%

:check
setenv -e
if %ERRORLEVEL% neq 0 (
	echo %date%:%time% - ERROR : setenv application is not installed >>%LOG_FILE%
	cls
	goto end)
7z
if %ERRORLEVEL% neq 0 (
	echo %date%:%time% - ERROR : 7z application is not installed >>%LOG_FILE%
	cls
	goto end)
:startInstallation
cls
echo.
echo JDK and JCE installation will start
echo.
pause
start /wait cmd /k CALL "Install JDK.bat"
cls
echo.
echo Derby and JBoss installtion will start
echo.
pause
start /wait cmd /k CALL "Install Derby-Jboss.bat"
cls
echo.
echo Installation Complete.
pause

:createReport
cls
echo OUTPUT FILE : %APP_DIR%\%OUT_FILE% >>%LOG_FILE%
echo DERBY_DIR - C:\derby-jar >%OUT_FILE%
echo JBOSS_DIR - C:\jboss >>%OUT_FILE%
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