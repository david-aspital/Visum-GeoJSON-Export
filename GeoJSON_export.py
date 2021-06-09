import pandas as pd
import json
import shapely.wkt
import shapely.geometry



def wkt2geometry(df, wkt_col):
    wkt_list = df[wkt_col].tolist()
    out_list = []
    for s in wkt_list:
        out_list.append(json.dumps(shapely.geometry.mapping(shapely.wkt.loads(s))))
    df['Geometry'] = out_list
    return df

def cols2properties(df, cols=None):
    if cols is None:
        cols = df.columns.values.tolist()
        cols.remove('WKTSURFACE')
    df['Properties'] = ""
    for i, row in df.iterrows():
        properties = {}
        for col in cols:
            properties[str(col)] = row[col]
        df.loc[i, 'Properties'] = json.dumps(properties)
    return df

def rows2features(df):
    df['Feature'] = '{"type": "Feature", "geometry": '+df.Geometry+', "properties": '+df.Properties+'}'
    return df
    

df = pd.read_csv('Test_data.att', sep='\t', encoding='latin1')
df2 = cols2properties(df)
df3 = wkt2geometry(df2,'WKTSURFACE')
df4 = rows2features(df3)
feature_list = df4['Feature'].tolist()
feature_collection = '{"type": "FeatureCollection",  "features": ['+','.join(feature_list)+']}'
test = json.loads(feature_collection)
with open('Test.geojson', 'w') as f:
    f.write(feature_collection)

