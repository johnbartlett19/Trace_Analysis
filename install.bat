@reg query "hklm\software\Python"  
@if ERRORLEVEL 1 GOTO NOPYTHON  
@goto :HASPYTHON  
:NOPYTHON  
@rem ActivePython-2.6.4.8-win32-x86.msi 
@echo: "Download and install latest version of Python 2.7.  This script is not compatible with Python 3."
@echo: "https://www.python.org/downloads"

:HASPYTHON
 
@REM Check user path to include python, add if not there
@set found=0
echo %PATH%; | find /C /I ";C:\Python27"
@set result1 = %ERRORLEVEL%
echo result = %result1%
@if result1==1 GOTO PATHSET
@echo "Setting PATH"
@REM set PATH=%PATH%;C:\Python27

:PATHSET
@REM Ensure we have the latest pip for installation
@REM C:\Python27\python -m pip install -U pip setuptools
REM C:\Python27\python -m pip install --upgrade pip 

@REM install modules needed:
REM @C:\Python27\python -m pip install dpkt matplotlib



 