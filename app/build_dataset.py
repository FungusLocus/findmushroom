import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from clean_mushroom_data import get_dataframe, finnish_coordinates
from shapely.geometry import box


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


# this function creates training dataset for each mushroom. Training set uses other 9 mushrooms as absence data (method: target group background).
def create_training_set():
    df = get_dataframe()
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["WGS84 E"], df["WGS84 N"]),crs=4326,).to_crs(3067)
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
        print(absence_df.nunique())
        
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
        
    return species_datasets
    # Usage: boletus_df = species_datasets['karvarousku']

def grids_over_finland():
    finland = finnish_coordinates().to_crs(3067)
    
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
    print(full_grid)
    
    return full_grid
    

if __name__ == "__main__":
    create_training_set()
    # grids_over_finland()