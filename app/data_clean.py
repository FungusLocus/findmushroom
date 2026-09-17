import pandas as pd
import numpy

# This file will handle data cleaning


def clean_weather_data():
    pass


def clean_mushroom_data():
    pass


def open_mushroomdata():
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
        df = pd.read_csv(f'datasets/{shroom}.tsv', sep='\t')
        print(df)


if __name__ == "__main__":
    open_mushroomdata()
