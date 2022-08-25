:: This .bat file install:
::  1) Python 3.9.7 if other Python is not exist in system
::  2) venv in the same with .bat folder
::  3) activate venv and install missing packages
:: For venv_install.bat script to work correctly,
:: it's needs 2 files in the same folder:
::  1) venv_handler.py
::  2) python-3.9.7-amd64.exe

@echo off
:: Check of Python exists
for /F "delims= " %%i in ('py -V') do (
    set pyexist=%%i
)
echo %pyexist%
if exist "venv\Scripts\activate.bat" (
    venv\Scripts\activate.bat && py -m venv_handler
) else (

	:: Behaveour if Python is not exist 
	if /I "%pyexist%" neq "Python" (
        	echo Installation of Python 3.9.7
        	python-3.9.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        	echo Python 3.9.7 is installed
    	)

    :: Install venv and packages
    py -m venv_handler --venvinstall
    venv\Scripts\activate.bat && py -m venv_handler
)
pause