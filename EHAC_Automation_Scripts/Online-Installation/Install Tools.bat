@echo off

set LOG_FILE=Tools-Install-Log.log
set DIR1="C:\Program Files (x86)"
set DIR2="C:\Program Files"
set SEARCH_TEXT="Mozilla Firefox"

echo ==============================================================>%LOG_FILE%

:checkAndInstallSetenv
setenv -e
if %ERRORLEVEL% neq 0 (
	cls
	echo %date%:%time% - INFO : Installing setenv application >>%LOG_FILE%
	echo Installing Setenv.......
	SetEnv_Setup.exe
	cls
	echo %date%:%time% - DEBUG : setenv application installation complete >>%LOG_FILE%
	echo Setenv application installation complete ) else (
		cls
		echo %date%:%time% - DEBUG : setenv application already installed  >>%LOG_FILE%
		echo setenv application already installed  )
pause
cls

:checkAndInstallPython
python -h
if %ERRORLEVEL% equ 9009 (
	cls
	echo %date%:%time% - INFO : Installing Python ..... >>%LOG_FILE%
	echo Installing Python .........
	python-2.7.6.amd64.msi
	cls
	echo %date%:%time% - DEBUG : Python Installtion Complete >>%LOG_FILE%
	echo Python Installtion Complete ) else (
		cls
		echo %date%:%time% - INFO : Python already Installed >>%LOG_FILE% 
		echo Python already Installed )
pause
cls

:checkAndInstall7z
7z
if %ERRORLEVEL% equ 0 (
	cls
	echo 7z application already installed
	echo %date%:%time% - IFNO : 7z application already installed >>%LOG_FILE% ) else (
		cls
		echo %date%:%time% - INFO : Installing 7z application....... >>%LOG_FILE%
		echo Installing 7z application.......
		7z920-x64.msi
		cls
		echo %date%:%time% - DEBUG : 7z application installation complete >>%LOG_FILE%
		echo 7z application installation complete )
pause
cls

:checkAndInstallFirefox
dir %DIR1% | findstr %SEARCH_TEXT%
if %ERRORLEVEL% equ 0 (
	echo %date%:%time% - INFO : Firefox Already Installed >>%LOG_FILE%
	goto end )

dir %DIR2% | findstr %SEARCH_TEXT%
if %ERRORLEVEL% equ 0 (
	echo %date%:%time% - INFO : Firefox Already Installed >>%LOG_FILE%
	goto end )
cls

echo %date%:%time% - INFO : Installing Firefox ..... >>%LOG_FILE%
echo Installing Firefox .....
call "Firefox Setup 21.0.exe"
cls
echo %date%:%time% - DEBUG : Firefox Installation Complete >>%LOG_FILE%
echo Firefox installation complete
pause
				
:end
cls
type %LOG_FILE%
echo.
pause
exit