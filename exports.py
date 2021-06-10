import os
import datetime
import pandas as pd


def export_list(list_func, lla, folderpath, filename, filter=False):
    # Create Visum list and export it to the given path
    visum_list = list_func
    visum_list.OpenLayout(lla)
    if filter:
        visum_list.SetObjects(filter)
    if filename[-4:] == ".att":
        pass
    else:
        name = name+".att"
    visum_list.SaveToAttributeFile(f"{folderpath}\\{filename}",9)
    visum_list.Close()
    visum_list = None


def create_data_frame(list_func, lla, folderpath, temp_path, filter=False):
    # Create pandas df from Visum list (export as att to temp path and read back)
    visum_list = None
    bkslsh = "\\"
    lla_path = os.path.join(folderpath, lla)
    temp_file = f"{lla_path.replace('.llax', '').replace('.lla', '')}_{datetime.datetime.now()}.att"
    export_list(list_func, lla_path, temp_path, temp_file, filter)
    data_frame = pd.read_csv(f"{temp_path}\\{temp_file}", sep="\t", header=2, skiprows=10, encoding='latin1')
    return data_frame