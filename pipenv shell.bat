cd /d %~dp0
@echo off
cd %

@echo on
echo Ejecutando ambiente virtual
echo Coloque luego: pipenv run main.py

pipenv shell

echo END
PAUSE