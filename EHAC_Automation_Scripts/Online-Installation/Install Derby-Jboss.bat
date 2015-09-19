@echo off

:installDerby
rmdir /S /Q %TMP_DIR%
rmdir /S /Q %DERBY_DIR%
cls
echo Extracting Derby at %DERBY_DIR%
chdir %DOWNLOAD_DIR%
7zG e %DERBY_FILENAME% -o%TMP_DIR%
7zG x %TMP_DIR%\derby.jar -o%DERBY_DIR%
chdir %APP_DIR%
echo %date%:%time% - INFO : Derby extracted to folder %DERBY_DIR% >>%LOG_FILE%
cls
echo Derby Extraction Complete
echo.
pause

:checkJbossService
cls
echo %date%:%time% - DEBUG : Checking if JBOSS is already installed >>%LOG_FILE%
sc query | findstr "JBoss"
if %ERRORLEVEL% equ 0 goto jbossOptions
sc qc %JBOSS_SERVICE1%
if %ERRORLEVEL% equ 0 goto jbossOptions
sc qc %JBOSS_SERVICE%
if %ERRORLEVEL% equ 0 goto jbossOptions
goto installJboss

:jbossOptions
echo Above Jboss Windows Service already exist
echo %date%:%time% - INFO : Jboss Windows Service already exist >>%LOG_FILE%
echo Jboss options
echo Option 1 - Reinstall Jboss
echo Option 2 - Continue with current Jboss install
set /p input="Please enter your option [1 or 2] : "
if "%input%" == "1" goto unInstallJboss
if not "%input%" == "1" goto end

:unInstallJboss
cls
echo Existing JBoss service will be stopped and deleted.
set /p input="Do you want to continue (Y or N) : "
if not %input%==Y (
	if not %input%==y goto end
	)
cls
echo %date%:%time% - DEBUG : Uninstalling Jboss Windows Service >>%LOG_FILE%
cls
sc qc %JBOSS_SERVICE1%
if %ERRORLEVEL% equ 0 set JBOSS_SERVICE_STOP=%JBOSS_SERVICE1%
sc qc %JBOSS_SERVICE%
if %ERRORLEVEL% equ 0 set JBOSS_SERVICE_STOP=%JBOSS_SERVICE%
cls
sc stop %JBOSS_SERVICE_STOP%
sc delete %JBOSS_SERVICE_STOP%

:installJboss
echo %date%:%time% - DEBUG : Installing Jboss Windows Service >>%LOG_FILE%
set JBOSS_BIN=%JBOSS_DIR%\jboss-as-7.1.1.Final\bin
cls
rmdir /S /Q %JBOSS_DIR%
rmdir /S /Q %TMP_DIR%
cls

echo Installing JBoss........
chdir %DOWNLOAD_DIR%
7zG x %JBOSS_FILENAME% -o%JBOSS_DIR%
7zG x %JBOSS_SSL_FILENAME% -o%TMP_DIR%

chdir %APP_DIR%
copy /Y %TMP_DIR%\bin\* %JBOSS_BIN%
echo %date%:%time% - INFO : Jboss extracted to folder %JBOSS_DIR% >>%LOG_FILE%
echo %date%:%time% - INFO : Jboss SSL files extracted >>%LOG_FILE%
echo %date%:%time% - INFO : Jboss SSL "bin" files copied to %JBOSS_BIN% >>%LOG_FILE%
cls
python edit_jboss_file.py %JBOSS_BIN%
if %ERRORLEVEL% equ 0 echo %date%:%time% - DEBUG : Jboss service.bat file edited >>%LOG_FILE%
if %ERRORLEVEL% neq 0 (
	echo %date%:%time% - ERROR : Error in editing Jboss service.bat file>>%LOG_FILE%
	echo Error while editing the service.bat file. Jboss Installation Failed
	pause
	goto error)

chdir %JBOSS_DIR%\jboss-as-7.1.1.Final\bin
CALL service.bat install
chdir %APP_DIR%
sc config %JBOSS_SERVICE%  start= auto
if %ERRORLEVEL% neq 0 (
	echo %date%:%time% - ERROR : Jboss Windows Service not found >>%LOG_FILE%
	goto error)
sc start %JBOSS_SERVICE%
echo %date%:%time% - DEBUG : Jboss Installed and service started >>%LOG_FILE%
goto end

:error
echo %date%:%time% - INFO : Jboss service could not be started due to above error>>%LOG_FILE%
goto end

:end
echo %date%:%time% - INFO : End of Derby and Jboss installtion >>%LOG_FILE%
rmdir /S /Q %TMP_DIR%
exit