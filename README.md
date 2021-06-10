# PTV Visum GeoJSON Export
Tool to export data from PTV Visum into GeoJSON format. Please contact [David Aspital](mailto:david.aspital@ptvgroup.com?subject=%5BGitHub%5D%20GeoJSON%20Export%20Tool), or log an issue if you have any queries about this tool.


## Introduction

GeoJSON is a format for encoding a variety of geographic data structures that is becoming increasingly popular as an alternative to ESRI Shapefiles. The full specification for GeoJSON can be found [here](https://datatracker.ietf.org/doc/html/rfc7946), but it is important to note that it is based on the World Geodetic System 1984 projection system.

PTV Visum does not currently offer a built-in exporter for data in GeoJSON format, so this tool has been developed as an add-in to pull data from a Visum .ver file using layout (.llax) files to define the data to be exported.


## Requirements
The tool requires the use of the `shapely` Python module which is not currently available with the standard PTV Visum installation. In order for the tool to run successfully, it is required that a Python environment is created that includes this module. It is suggested that [Anaconda](https://www.anaconda.com/) is used for this and `shapely` is installed in the environment.

This tool has been designed to work with Visum 2021, but can be simply updated to work with other versions of Visum. Users of this tool are assumed to be familiar with PTV Visum and Transport Modelling terminology. For more info about PTV Visum, please visit: https://www.ptvgroup.com/en/solutions/products/ptv-visum/.


## Running the Tool
There are two options for running the tool:
1. Within Visum as part of a model run 
2. External to Visum after a model has been run and saved

### Within Visum

The first option is designed to require minimal user intervention and be set up as a part of a standard model running procedure. It can be set up as a 'Run script' procedure that links to the `GeoJSON.py` file, with the layout files that define the data to be exported saved in a 'GeoJSON Layouts' folder in the same location as the script file. The only user intervention required to get the script to run is to update the folder path on **<span style="color:red"> line X </span>** with the location of the Python environment that contains `shapely`. The script will then export the data into the same folder as the version file.


### Outside of Visum
The second option is for processing data from a model that has already been run and saved. The script can be run externally to Visum from the environment in which `shapely` is installed. A file selection dialog will first appear in which the user should select the Visum version file, before a folder selection where the user can select the folder containing the layout files defining the data to be exported. The tool will then run and export the data into the same folder as the script.
