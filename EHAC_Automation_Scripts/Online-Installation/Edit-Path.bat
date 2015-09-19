@echo off
setenv -e
if %ERRORLEVEL% neq 0 (
	cls
	echo ERROR : setenv application is not installed.
	goto end )
cls
echo Adding required environment path....
setenv -a path %%"C:\Python27"
setenv -a path %%"C:\Program Files\7-Zip"
setenv -a path %%"C:\Python27\Scripts"
echo Please wait till the timeout completes
timeout /t 5 /NOBREAK
:end
pause
exit