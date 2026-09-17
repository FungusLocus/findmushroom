import pandas as pd
import numpy as np


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

    # Dropping unneeded columns
    df = df.drop(['The stated certainty of the observation',
                  'Observation Reliability',
                  'Municipality',
                  'Collection'], axis=1)

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
    # print(df[df['Time'].isna()])
    # print(df['Time'].unique())
    
    # Need to add column for classification 1/0
    # Ask about number, province and country columns
    # Check that coordinate columns legit :)
    
    print(df)

def open_mushroomdata():
    # opening each mushroom file and adding them together into one df, returns
    # that df unedited
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


if __name__ == "__main__":
    df = open_mushroomdata()
    clean_mushroom_data(df)
