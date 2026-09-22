import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

def get_dataframe():
    df = open_mushroomdata()
    df = clean_mushroom_data(df)
    return df

def finnish_coordinates():
    finland = gpd.read_file("datasets/gadm41_FIN.gpkg", layer="ADM_ADM_0") 
    # print(finland.total_bounds)
    return finland

def open_mushroomdata():
    # opening each mushroom file and adding them together into one df, returns that df unedited
    length = 0
    mushrooms = [
        'herkkutatti',
        'karvarousku',
        'keltavahvero',
        'korvasieni',
        'lampaankaapa',
        'mustatorvisieni',
        'mustavahakas',
        'sikurirousku',
        'suppilovahvero',
        'vaaleaorakas']
    for shroom in mushrooms:
        if shroom == 'herkkutatti':
            mushroom_df = pd.read_csv(f'datasets/{shroom}.tsv', sep='\t')
            length += len(mushroom_df)
        else:
            df = pd.read_csv(f'datasets/{shroom}.tsv', sep='\t')
            mushroom_df = pd.concat([mushroom_df, df], ignore_index=True)
            length += len(df)
    # print(mushroom_df)

    # checking that each row got added
    # print(length)

    return mushroom_df

def map_mushroom_names(df):
    latin_to_finnish = {}
    for val in df['Species'].dropna().unique():
        if '—' in val:
            fi_part, latin_part = val.split('—')
            fi_name = fi_part.split('(fi)')[0].strip()
            latin_to_finnish[latin_part.strip()] = fi_name

    # print(latin_to_finnish)
    # print(len(latin_to_finnish))

    return latin_to_finnish

def clean_mushroom_data(df):
    # selecting rows where observer is sure or observation is verified by
    # expert or community
    df = df[(df['The stated certainty of the observation'] == 'Sure') | 
            (df['Observation Reliability'].isin(['COMMUNITY_VERIFIED', 'EXPERT_VERIFIED']))]

    # print(len(df))

    # Dropping nuisance columns
    df = df.drop(['The stated certainty of the observation',
                  'Observation Reliability',
                  'Municipality',
                  'Collection', 'Number', 'Biogeographical Province', 'Country'], axis=1)

    # Mapping translations
    translates = map_mushroom_names(df)

    # claen Species column to only have latin name
    df['Species'] = df['Species'].apply(lambda x: x.split('—')[1].strip() if '—' in x else x)
    df = df.replace({"Species": "kantarelli (kuvassa myös yksi valevahvero)"},"Cantharellus cibarius")
    df = df.replace({"Species": "Lactarius camphoratus (Bull.) Fr."},"Lactarius camphoratus")
    df = df.replace({"Species": "Cantharellus cibarius Fr."},"Cantharellus cibarius")
    df = df.replace({"Species": "Hygrophorus camarophyllus (Alb. & Schwein.) Dumée, Grandjean & Maire"},"Hygrophorus camarophyllus")
    
    #Fix Vernacular name column from NaN values and make the column just have the finnish name without any extras
    df['Vernacular name'] = df['Vernacular name'].fillna(df['Species'].map(translates))
    df['Vernacular name'] = df['Vernacular name'].apply(lambda x: x.split(' ')[0].strip() if ' ' in x else x)

    # Fixing time column to have just date
    df['Time'] = df['Time'].apply(lambda x: x.split(' ')[0].strip() if ' ' in x else x)
    
    # Time column into datetime object:
    df["Time"] = pd.to_datetime(df["Time"])
    
    # print(df[df['Time'].isna()])
    # print(df['Time'].unique())
    
    # Delete rows with missing values
    df = df.dropna()
    
    # print(df.isnull().sum())

    # print(df)
    
    return df


def plot_months():
    df = get_dataframe()
    months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',' December']
    monthly_counts = df["Time"].dt.month_name().value_counts().reindex(months)

    plt.figure(figsize=(10, 5))
    bars = plt.bar(monthly_counts.index, monthly_counts.values, color="lightblue")
    
    plt.xlabel("Month")
    plt.ylabel("Observations")

    plt.tight_layout()
    plt.show()
    
    
def plot_observations(): # need to take care of the outliers
    finland = finnish_coordinates()
    df = get_dataframe()

    obs_gdf = gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df["WGS84 E"], df["WGS84 N"]),crs="EPSG:4326")

    fig, ax = plt.subplots(figsize=(8, 10))
    finland.plot(ax=ax, color="#f0f0f0", edgecolor="black")
    obs_gdf.plot(ax=ax, markersize=3, alpha=0.5, color="darkgreen")
    ax.set_title("Mushroom observations")
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # df = open_mushroomdata()
    # df = clean_mushroom_data(df)
    plot_months()
    # plot_observations()
