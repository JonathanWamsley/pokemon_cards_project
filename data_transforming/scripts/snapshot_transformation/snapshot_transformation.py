import pandas as pd
import numpy as np
import json
import re
from itertools import zip_longest
from datetime import date

def create_pokemon_list(date):
    file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/pokemon_cards/' \
        f'scraped_data/pokemon_list_2020-03-24.json'
    with open(file_path) as f:
        raw_data = json.load(f)
    pokemon_list = raw_data[0]['pokemon_list']
    pokemon_list[28] = 'Nidoran F'
    pokemon_list[31] = 'Nidoran M'
    pokemon_list[668] = 'Flabebe'

    pokemon_list_df = pd.DataFrame(data=pokemon_list, columns=['Pokemon Name'])
    return pokemon_list_df


def create_pokemon_set(date):
    file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/pokemon_cards/' \
        f'scraped_data/pokemon_sets_2020-03-24.json'
    with open(file_path) as f:
        raw_data = json.load(f)

    set_name = raw_data[0]['set_name']
    set_date = raw_data[0]['set_date']
    set_abr = raw_data[0]['set_abbreviation']

    # removes blank lines
    set_name = list(filter(None, set_name))
    set_date = list(filter(None, set_date))
    set_abr = list(filter(None, set_abr))

    # sometimes a new set is known but the abr or release date is not
    if len(set_date) < len(set_name):
        set_date.append('')
    if len(set_abr) < len(set_name):
        set_abr.append('')

    pokemon_set_df = pd.DataFrame(np.array([set_name, set_date, set_abr]).T,
                                  columns=['Set Name', 'Set Date', 'Set Abr'])
    pokemon_set_df['Set Name'] = pokemon_set_df['Set Name'].str.replace('&', 'and')
    return pokemon_set_df


def create_pokemon_cards(date):
    df = load_pokemon_cards(date)
    df_clean = clean_pokemon_cards(df)
    df_tags = add_pokemon_tags(df_clean)
    df_concat = combined_data_sources(df_tags)



 def load_pokemon_cards(data):
    file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/pokemon_cards/scraped_data/pokemon_cards_2020-03-24.json'
    df = pd.read_json(file_path)
    return df

def clean_pokemon_cards(df):
    df.dropna(subset=['Card Name'], inplace=True)
    df.drop(columns=['Presale Information'], inplace=True)
    df.reset_index(inplace=True)
    df.loc[df['Stage'] == 'bASIC', 'Stage'] = 'Basic'
    return df

def add_pokemon_tags(df):
    df_tag_1 = is_pokemon_tag(df)
    def_tag_2 = card_id_tag(df_tag_1)


def is_pokemon_tag(df):
    not_pokemons_keys = ['Energy', 'Trainer', 'Special Energy', 'Stadium', 'Technical Machine', 'Item', '', 'Tool',
                         'Supporter']
    pokemon_bool_1 = ~df['Stage'].isin(not_pokemons_keys)
    pokemon_bool_2 = ~df['Stage'].isna()
    pokemon_bool = pokemon_bool_1 & pokemon_bool_2
    df['Is Pokemon'] = pokemon_bool
    return df

def card_id_tag(df):
    df['Card Id'] = df['Card Name'].map(str) + df['Set Name'].map(str) + df['Card Number'].map(str)
    return df


def combined_data_sources(df):
    df_combined_sets = combine_sets(df)
    df_combined_list = combine_list(df)

def combine_sets(df):
    pc_set = set(df['Set Name'])  # there are some weird name conventions that are going to need to be renamed
    pokemon_set = set(pokemon_set_df['Set Name'])  # this the benchmark for what a set name should look like
    sets_dic = {
        'Crystal Guardians': 'EX Crystal Guardians',
        'Delta Species': 'EX Delta Species',
        'Deoxys': 'EX Deoxys',
        'Dragon': 'EX Dragon',
        'Dragon Frontiers': 'EX Dragon Frontiers',
        'Emerald': 'EX Emerald',
        'FireRed & LeafGreen': 'EX FireRed and LeafGreen',
        'Hidden Legends': 'EX Hidden Legends',
        'Holon Phantoms': 'EX Holon Phantoms',
        'Legend Maker': 'EX Legend Maker',
        'Power Keepers': 'EX Power Keepers',
        'Ruby and Sapphire': 'EX Ruby and Sapphire',
        'Sandstorm': 'EX Sandstorm',
        'Team Magma vs Team Aqua': 'EX Team Magma vs Team Aqua',
        'Team Rocket Returns': 'EX Team Rocket Returns',
        'Unseen Forces': 'EX Unseen Forces',
        'XY Base Set': 'XY',
        'SM Base Set': 'Sun and Moon',
        'HeartGold SoulSilver': 'HeartGold and SoulSilver',
        'Expedition': 'Expedition Base Set',
        'XY - Ancient Origins': 'Ancient Origins',
        'XY - BREAKpoint': 'BREAKpoint',
        'XY - BREAKthrough': 'BREAKthrough',
        'SM - Burning Shadows': 'Burning Shadows',
        'SM - Celestial Storm': 'Celestial Storm',
        'SM - Crimson Invasion': 'Crimson Invasion',
        'XY - Evolutions': 'Evolutions',
        'XY - Fates Collide': 'Fates Collide',
        'XY - Flashfire': 'Flashfire',
        'SM - Forbidden Light': 'Forbidden Light',
        'XY - Furious Fists': 'Furious Fists',
        'SM - Guardians Rising': 'Guardians Rising',
        'SM - Lost Thunder': 'Lost Thunder',
        'XY - Phantom Forces': 'Phantom Forces',
        'XY - Primal Clash': 'Primal Clash',
        'XY - Roaring Skies': 'Roaring Skies',
        'XY - Steam Siege': 'Steam Siege',
        'SM - Team Up': 'Team Up',
        'SM - Ultra Prism': 'Ultra Prism',
        'SM - Unbroken Bonds': 'Unbroken Bonds',
        'SM - Unified Minds': 'Unified Minds',
        'SM - Cosmic Eclipse': 'Cosmic Eclipse',
        'SWSH01: Sword & Shield Base Set': 'Sword and Shield',
    }
    df['Set Name'].replace(sets_dic, inplace=True)
    pc_set = set(df['Set Name'])

    not_expansion = pd.DataFrame(list(pc_set - pokemon_set), columns=[
        'Set Name'])  # investigating this sets show that they are promotion, tournament winning cards, error cards

    pokemon_set_table = pokemon_set_df.append(not_expansion, sort=False)
    pokemon_set_table.reset_index()





if __name__ == "__main__":
    current_date = date.today()
    pokemon_list_df = create_pokemon_list(current_date)
    pokemon_set_df = create_pokemon_set(current_date)
    pokemon_cards_df = create_pokemon_cards(current_date)
