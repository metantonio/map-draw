echo Carpeta de Instalacion de dependencias

cd /d %~dp0
@echo off
cd %

@echo on
pip install --user pipenv
pipenv install

echo END
PAUSE