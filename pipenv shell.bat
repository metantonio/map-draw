echo Ejecutando ambiente virtual
echo Coloque luego: pipenv run main.py

cd /d %~dp0
@echo off
cd %

@echo on
pipenv shell

echo END
PAUSE