import pandas as pd
import numpy as np
import geopandas as gpd

def get_station_data():
    df = open_station_data()
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["latitude"], df["longitude"]),crs=4326,).to_crs(3067)
    return gdf

def get_weather_data():
    df = clean_data()
    return df

def open_weather_data():
    df = pd.read_csv('datasets/filled_all.csv')
    return df
    
def open_station_data():
    df = pd.read_csv('datasets/stations.csv')
    return df

def clean_data():
    weather = open_weather_data()
        
    weather = pd.wide_to_long(weather, stubnames=['prec', 'temp'], i='time', j='station', sep='_', suffix=r'[\w-]+').reset_index()
    weather["time"] = pd.to_datetime(weather["time"])
    weather = weather.sort_values(['station', 'time']).reset_index(drop=True)
    weather['prec_7d'] = weather.groupby('station')['prec'].transform(lambda x: x.rolling(window=7, min_periods=1).sum())
    weather['prec_14d'] = weather.groupby('station')['prec'].transform(lambda x: x.rolling(window=14, min_periods=1).sum())
    weather['temp_7d_avg'] = weather.groupby('station')['temp'].transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    weather['temp_14d_avg'] = weather.groupby('station')['temp'].transform(lambda x: x.rolling(window=14, min_periods=1).mean())

    # df = pd.merge(weather,stations[['name', 'latitude', 'longitude']], left_on='station', right_on='name',how='left')
    # df = df.drop(columns=['name'])
    # print(weather)
    # print(df)
    # print(df.isnull().sum())
    # print(gdf)
    
    return weather


if __name__ == "__main__":
    # open_weather_data()
    # open_station_data()
    clean_data()