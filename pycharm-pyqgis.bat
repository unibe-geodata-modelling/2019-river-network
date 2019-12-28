SET OSGEO4W_ROOT=C:\OSGeo4W
SET QGISNAME=qgis
SET QGIS=%OSGEO4W_ROOT%\apps\%QGISNAME%
SET QGIS_PREFIX_PATH=%QGIS%
SET PYCHARM="C:\Program Files\JetBrains\PyCharm Community Edition 2019.2.3\bin\pycharm64.exe"

CALL %OSGEO4W_ROOT%\bin\o4w_env.bat

SET PATH=%PATH%;%QGIS%\bin
SET PYTHONPATH=%QGIS%\python;%PYTHONPATH%

start "PyCharm aware of QGIS" /B %PYCHARM% %*