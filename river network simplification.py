# river network modelling
# seminar on geodata analysis and modelling, University of Bern, spring semester 2019
# Mukadem Brumand & Carine Hürbin
# supervised by Andreas Zischg, Pascal Horton and Jorge Ramirez
# language: English

# import QGIS interface
from PyQt5.QtCore import *
from qgis.core import *

# library imports
import os
from osgeo import gdal
import rasterio
from geopandas import GeoDataFrame

# set working directory
os.chdir(r'C:\Users\Carine\PycharmProjects\untitled2')

# initialise QGIS interface
qgs = QgsApplication([], False)
QgsApplication.setPrefixPath(r'C:\Program Files\QGIS 3.10\bin\qgis-bin.exe', True)
qgs.initQgis()

# load layers in QGIS
vLayer1 = QgsVectorLayer(r'C:\Users\Carine\PycharmProjects\untitled2\CH river network without lakes.shp',
                         "CH river network", "ogr")
print(vLayer1.isValid())

vLayer2 = QgsVectorLayer(r'C:\Users\Carine\PycharmProjects\untitled2\measuringGauges.shp', "measuring Gauges", "ogr")
print(vLayer2.isValid())

# load raster file
fileName = r'C:\Users\Carine\PycharmProjects\untitled2\dem_ch25.asc'
fileInfo = QFileInfo(fileName)
baseName = fileInfo.baseName()
rLayer = QgsRasterLayer(fileName, baseName)
print(rLayer.isValid())


# node extraction - branching of all rivers, sources and rivulets
# extract nodes function from QGIS plugin Processing
# Generate list of QgsPoints from input geometry (can be point, line, or polygon)

def extractpoints(geom):
    temp_geom = []
    if geom.type() == 0:  # it's a point
        if geom.isMultipart():
            temp_geom = geom.asMultiPoint()
        else:
            temp_geom.append(geom.asPoint())
    elif geom.type() == 1:  # it's a line
        if geom.isMultipart():
            multi_geom = geom.asMultiPolyline()  # multi_geog is a multiline
            for i in multi_geom:  # i is a line
                temp_geom.extend(i)
        else:
            temp_geom = geom.asPolyline()
    elif geom.type() == 2:  # it's a polygon
        if geom.isMultipart():
            multi_geom = geom.asMultiPolygon()  # multi_geom is a multipolygon
            for i in multi_geom:  # i is a polygon
                for j in i:  # j is a line
                    temp_geom.extend(j)
        else:
            multi_geom = geom.asPolygon()  # multi_geom is a polygon
            for i in multi_geom:  # i is a line
                temp_geom.extend(i)
    # FIXME - if there is no known geometry (either point, line, or polygon), show a warning message
    return temp_geom


points = extractpoints(feature.geometry())


# calculating the slope from the raster file
def calculate_slope(dem):
    gdal.DEMProcessing('dem_ch25.asc', dem, 'slope')
    with rasterio.open('dem_ch25.asc') as dataset:
        slope = dataset.read(1)
    return slope


def calculate_aspect(dem):
    gdal.DEMProcessing('dem_ch25.asc', dem, 'aspect')
    with rasterio.open('dem_ch25.asc') as dataset:
        aspect = dataset.read(1)
    return aspect


slope = calculate_slope('dem_ch25.asc')
aspect = calculate_aspect('dem_ch25.asc')

print(type(slope))
print(slope.dtype)
print(slope.shape)

# simplify the river network shapefile with keeping the nodes
GeoDataFrame.simplify(vLayer1, 0.2, preserve_topology=True)

# write, modified shapefile under new name. Thus the simplified information will be saved separately.
_writer = QgsVectorFileWriter.writeAsVectorFormat("CH river network", "simplified river network", 'utf-8',
                                                  driverName='ESRI Shapefile')

# call exitQgis() to remove the provider and layer registries from memory
qgs.exitQgis()

print("simplification sucessfully done!")
