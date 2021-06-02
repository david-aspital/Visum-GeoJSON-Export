import pandas as pd
import json
import shapely.wkt
import shapely.geometry


def wkt2geojson(df, wkt_col):
    wkt_list = df[wkt_col].tolist()
    out_list = []
    for s in wkt_list:
        out_list.append(json.dumps(shapely.geometry.mapping(shapely.wkt.loads(s))))
    df['GeoJSON_Feature'] = out_list
    return df

df = pd.read_csv('Test_data.att', sep='\t', encoding='latin1')

df2 = wkt2geojson(df,'WKTSURFACE')


print(df2)