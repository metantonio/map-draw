echo Carpeta de Instalacion de dependencias

cd /d %~dp0
@echo off
cd %

@echo on
pip install --user branca
pip install colorama
pip install folium
pip install future
pip install geocoder
pip install matplotlib
pip install mpu
pip install numpy
pip install openpyxl
pip install pandas
pip install pillow
pip install pyparsing
pip install pyproj
pip install python-dateutil
pip install pyinstaller
pip install python-math
pip install request
pip install urlib3
pip install xlrd
pip install gevent
pip install nbconvert
pip install importlib-metadata
pip install jsonschema
pip install branca

echo END
PAUSE