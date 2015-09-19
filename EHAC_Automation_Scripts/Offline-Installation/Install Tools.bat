@echo off

set LOG_FILE=Tools-Install-Log.log

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

:end
cls
type %LOG_FILE%
echo.
pause