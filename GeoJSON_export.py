import json
import sys
import os
import glob
import tempfile
import pandas as pd
import win32com.client
import shapely.wkt
import shapely.geometry
from pathlib import Path
import exports as exp
import dialogs as dlg
import xml.etree.ElementTree as ET

Visum = None

wkt_col_names = ['WKTPOLYWGS84', 'WKTLOCWGS84', 'WKTSURFACEWGS84']
visum_lists = {'ZONE' : Visum.Lists.CreateZoneList,
               'LINK' : Visum.Lists.CreateLinkList,
               'NODE' : Visum.Lists.CreateNodeList}

def wkt2geometry(df, wkt_col):
    # Create list of WKT values, apply conversion to geometry and create new column
    wkt_list = df[wkt_col].tolist()
    out_list = []
    for s in wkt_list:
        out_list.append(json.dumps(shapely.geometry.mapping(shapely.wkt.loads(s))))
    df[f'Geom_{wkt_col}'] = out_list
    return df

def cols2properties(df, cols=None):
    # Convert data columns to properties
    if cols is None:
        cols = df.columns.values.tolist()
        for col in wkt_col_names:
            try:
                cols.remove(col)
            except  ValueError:
                pass
    df['Properties'] = ""
    for i, row in df.iterrows():
        properties = {}
        for col in cols:
            properties[str(col)] = row[col]
        df.loc[i, 'Properties'] = json.dumps(properties)
    return df

def rows2features(df, wkt_col):
    # Create features from geometries and properties
    df[f'Feat_{wkt_col}'] = '{"type": "Feature", "geometry": '+df[f'Geom_{wkt_col}']+', "properties": '+df.Properties+'}'
    return df

def get_llax_files(folder):
    # Get list of all .llax files in a folder
    llax_files = [f for f in glob.glob(f'{folder}\\*.llax')]
    return llax_files

def get_visum_object(llax):
    # Get Visum object from .llax file
    root = ET.parse(llax).getroot()
    for tag in root.findall('listLayoutItem/listLayoutCommonEntries'):
        obj = tag.get('layoutIdentifier').replace('LIST_LAYOUT_')
    return obj

def get_wkt_cols(df):
    # Finds WKT columns in the dataframe
    cols = df.columns.values.tolist()
    wkt_cols = [x for x in cols if x in wkt_col_names]

    if wkt_cols == []:
        raise KeyError("No valid WKT columns found. Please check the layout file and ensure that the WGS84 variants are used.")
    return wkt_cols

def process_llax(llax, Visum, temp_path, filter=False):
    obj = get_visum_object(llax)
    df = exp.create_data_frame(visum_lists[obj], llax, temp_path, filter)
    wkt_cols = get_wkt_cols(df)
    df = cols2properties(df)
    for col in wkt_cols:
        df = wkt2geometry(df, col)
        df = rows2features(df, col)
        feature_list = df[f'Feat_{col}'].tolist()
        feature_collection = '{"type": "FeatureCollection",  "features": ['+','.join(feature_list)+']}'
        output = json.loads(feature_collection)
        if len(wkt_cols) > 1:
            out_name = f'{llax}_{col.replace("WKT","").replace("WGS84", "")}.geojson'
        else:
            out_name = f'{llax}.geojson'
        with open(out_name, 'w') as f:
            f.write(json.dumps(feature_collection, indent=4, sort_keys=True))


def export_from_current(temp_path):
    sys.path.append(f"C:\\Users\\{os.getusername()}\\Anaconda3\\envs\\GeoJSON\\Lib\\site-packages")

    llax_folder = os.path.join(os.path.dirname(Visum.IO.CurrentVersionFile), 'GeoJSON llax')

    # Get llax files for processing
    llax_files = get_llax_files(llax_folder)

    # Loop through llax files and export data
    for llax in llax_files:
        process_llax(llax, Visum, temp_path)

def export_from_version(visum_versionNo, temp_path):
    # 

    # Select ver path and llax folder path
    ver_path = dlg.file_select_dlg("Please select a Visum version file...", "Version |*.ver")
    llax_folder = dlg.folder_select_dlg("Please select a folder containing layout files...",os.curdir())

    # Get llax files for processing
    llax_files = get_llax_files(llax_folder)
    
    # Launch Visum 
    Visum = win32com.client.Dispatch(f"Visum.Visum.{visum_versionNo}")
    Visum.IO.LoadVersion(ver_path)

    # Loop through llax files and export data
    for llax in llax_files:
        process_llax(llax, Visum, temp_path)

    # Close Visum to exit
    Visum = None


if __name__ == "__main__":

    temp_path = f"{tempfile.gettempdir()}\\Visum_GeoJSON"
    Path(temp_path).mkdir(parents=True, exist_ok=True)

    if 'Visum' in globals():
        export_from_current(Visum=Visum, temp_path=temp_path)
    else:
        export_from_version(visum_versionNo=21, temp_path=temp_path)


