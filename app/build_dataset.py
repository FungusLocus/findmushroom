import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from clean_mushroom_data import get_geodataframe, finnish_coordinates
from clean_weather_data import get_weather_data, get_station_data
from shapely.geometry import box

def csv_out(df):
    df.to_csv("datasets/train.csv", index=False)
    return
    
def create_grid_coordinates(gdf):
    grid_size = 5000
    gdf['grid_x'] = (gdf.geometry.bounds['minx'] // grid_size).astype(int)
    gdf['grid_y'] = (gdf.geometry.bounds['miny'] // grid_size).astype(int)
    
    return gdf

# thins the training data to lower the density bias
def spatial_thinning(gdf, size):
    
    gdf = create_grid_coordinates(gdf)
    # print(gdf)
    thinned_gdf = gdf.groupby(["Species", "grid_x", "grid_y"], group_keys=False).sample(n=1, random_state=42).reset_index(drop=True)
    # print(thinned_gdf)

    return thinned_gdf

def join_datasets():
    weather = get_weather_data() #not in gdf
    species = get_geodataframe()
    stations = get_station_data()
    
    # print(weather)
    # print(species)
    # print(stations)
    
    species = filter_weeks(species)
    
    species_with_station = gpd.sjoin_nearest(species, stations[["Station", "geometry"]], how="left", distance_col="distance_meters")
    species_with_station = species_with_station[~species_with_station.index.duplicated(keep='first')]
    
    df = pd.merge(species_with_station, weather, left_on=['Station', 'Time'], right_on=['Station', 'Time'], how='inner')
    # print(df.columns)
    # print(df['distance_meters'])
    # print(df['distance_meters'].max())
    # print(df['distance_meters'].min())
    # print(df['distance_meters'].median())
    # See how many rows have distances greater than certain thresholds
    df = df.drop(columns=['index_right'])
    # plot_distance_distribution(df)     
    # print(df.isnull().sum())
    df = df.dropna()
    # print(df.isnull().sum())
    # print(df)
    # print(df.columns)
    csv_out(df)    
    # print(df['Station'].nunique())

    return df


# this function creates training dataset for each mushroom. Training set uses other 9 mushrooms as absence data (method: target group background).
def create_training_set():
    gdf = join_datasets()
    # print(gdf)
    grid_size=5000
    
    thinned_gdf = spatial_thinning(gdf, grid_size)

    species_list = gdf["Vernacular name"].unique()
    # print(species_list)
    species_datasets = {}
    
    # For every species we build own training set
    for species in species_list:
        presence_df = thinned_gdf[thinned_gdf["Vernacular name"] == species].copy()
        presence_df["observed"] = 1

        absence_df = thinned_gdf[thinned_gdf["Vernacular name"] != species].drop_duplicates(subset=['grid_x', 'grid_y']).copy()
        absence_df["observed"] = 0
        # print(absence_df.nunique())
        
        presence_grids = set(zip(presence_df["grid_x"], presence_df["grid_y"]))
        
        absence_df["grid_tuple"] = list(zip(absence_df["grid_x"], absence_df["grid_y"]))
        absence_df = absence_df[~absence_df['grid_tuple'].isin(presence_grids)]
        
        final_df = pd.concat([presence_df, absence_df], ignore_index=True)
        final_df = final_df.drop(["grid_tuple"], axis=1)
        
        # absence_df = (thinned_gdf[thinned_gdf["Vernacular name"] != species].drop_duplicates(subset=["grid_x", "grid_y"]).copy())
        # absence_df["observed"] = 0
        
        species_datasets[species] = final_df
        # print(final_df['observed'].value_counts())
    
    # print(species_datasets)
    # print(species_datasets['karvarousku'].columns)
    return species_datasets

def grids_over_finland():
    finland = finnish_coordinates().to_crs(3067)
    stations = get_station_data() #112 stations
    # print(stations['Station'].nunique())
    
    grid_size = 5000
    min_x, min_y, max_x, max_y = finland.total_bounds
    
    min_x = (min_x // grid_size) * grid_size
    min_y = (min_y // grid_size) * grid_size
    
    cells = [
        box(x, y, x + grid_size, y + grid_size)
        for x in np.arange(min_x, max_x, grid_size)
        for y in np.arange(min_y, max_y, grid_size)]
    
    full_grid = gpd.GeoDataFrame(geometry=cells, crs=3067)
    # print(full_grid)
    full_grid = gpd.sjoin(full_grid, finland[['geometry']], predicate='intersects').drop(columns='index_right')
    # print(full_grid)
    
    
    full_grid = create_grid_coordinates(full_grid)
    full_grid = full_grid.reset_index(drop=True)
    
    df = gpd.sjoin_nearest(full_grid, stations[["Station", "geometry"]], how="left", distance_col="distance_meters")
    df = df[~df.index.duplicated(keep='first')] 
    # print(df['Station'].nunique()) # 108 --> 4 stations out
    return df

def make_prediction_table_for_grids():
    full_grid = grids_over_finland()
    weather = get_weather_data()
    weekly = weekly_weather_avgs(weather)
    # print(full_grid) 
    df = pd.merge(full_grid, weekly, left_on=['Station'], right_on=['Station'], how='left')
    # print(df['Station'].nunique())
    # print(df)
    # print(df.columns)
    df = df.drop(columns=['index_right', 'distance_meters'])
    # print(df.isna().sum()) 
    return df

def weekly_weather_avgs(data):
    df = data.copy()
    df = filter_weeks(df)
    df = df.groupby(['Station', 'week'])[['prec', 'temp', 'prec_7d', 'prec_14d', 'temp_7d', 'temp_14d']].mean().reset_index()  
    print('weekly function', df['Station'].nunique())
    return df

def filter_weeks(df):
    species = get_geodataframe()
    week_counts = species["Time"].dt.isocalendar().week.value_counts()
    valid_weeks = week_counts[week_counts >= 50].index.tolist()
    
    # df['week'] = pd.to_datetime(df["Time"]).dt.isocalendar().week
    # df = df[df["week"].isin(valid_weeks)]
    print(min(valid_weeks))
    print(max(valid_weeks))
    
    return df

def plot_distance_distribution(df):
    dist = df['distance_meters'] / 1000
    fig, ax = plt.subplots(figsize=(8, 5))

    n, bins, patches = ax.hist(dist, bins=30, edgecolor='white', linewidth=1.2)
    ax.set_xlabel('Distance')
    ax.set_ylabel('Number of Mushroom Observations')

    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # create_training_set()
    # grids_over_finland()
    # join_datasets()
    # make_prediction_table_for_grids()
    filter_weeks(None)