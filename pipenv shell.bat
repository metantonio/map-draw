cd /d %~dp0
@echo off
cd %

@echo off
cls
echo Ejecutando ambiente virtual
echo Coloque luego: pipenv run main.py

pipenv shell

echo END
PAUSE