@echo off

set JDK_FILENAME=%1%
set JCE_FILENAME=%2%
set DERBY_FILENAME=%3%
set JBOSS_FILENAME=%4%
set JBOSS_SSL_FILENAME=%5%


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
exit
