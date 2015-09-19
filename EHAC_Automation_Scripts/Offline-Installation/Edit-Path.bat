@echo off
setenv -e
if %ERRORLEVEL% neq 0 (
	cls
	echo ERROR : setenv application is not installed.
	goto end )
cls
echo Adding required environment path....
setenv -a path %%"C:\Program Files\7-Zip"
echo Please wait till the pathtimeout completes
timeout /t 5 /NOBREAK
:end
pause
exit