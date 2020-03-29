import pandas as pd
import numpy as np
import json
import re
from itertools import zip_longest
from datetime import date


def create_pokemon_list():
    """loads the pokemon list data that was scraped, cleans it, and converts it to a pandas DataFrame

    Args:
        None

    Returns:
        DataFrame: a DataFrame of the pokemon list
    """
    pokemon_list = load_pokemon_list()
    pokemon_list_clean = clean_pokemon_list(pokemon_list)
    pokemon_list_column = 'pokemon_list'
    pokemon_list_df = pd.DataFrame(data=pokemon_list_clean, columns=['Pokemon Name'])
    return pokemon_list_df


def load_pokemon_list():
    """ provides correct data path to be opened and extracted

    Args:
        file_path (str): The file location of the JSON

    Returns:
        list: the pokemon names
    """
    pokemon_list_file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards' \
        f'/pokemon_cards/scraped_data/pokemon_list_2020-03-24.json'
    pokemon_list_raw = load_data(pokemon_list_file_path)
    pokemon_list_column = 'pokemon_list'
    pokemon_list = pokemon_list_raw[0][pokemon_list_column]
    return pokemon_list

def load_data(file_path):
    """Opens and returns a json file at target file path

    Args:
        file_path (str): The file location of the JSON

    Returns:
        list of dictionaries: The whole JSON object
    """
    with open(file_path) as f:
        raw_data = json.load(f)
    return raw_data


def clean_pokemon_list(pokemon_list):
    """cleans pokemon names that have weird symbols

    Args:
        pokemon_list (list): The pokemon list to clean

    Returns:
        list: a cleaned pokemon list
    """
    # Each pokemon has a pokedex ID. New pokemon are appended, So they will always have the same number
    POKEMON_NIDORAN_F = 28
    POKEMON_NIDORAN_M = 31
    POKEMON_FLABEBE = 668
    pokemon_list[POKEMON_NIDORAN_F] = 'Nidoran F'
    pokemon_list[POKEMON_NIDORAN_M] = 'Nidoran M'
    pokemon_list[POKEMON_FLABEBE] = 'Flabebe'
    return pokemon_list


pokemon_list_df = create_pokemon_list()


def create_pokemon_set():
    """loads the pokemon set data that was scraped, cleans it, and converts it to a pandas DataFrame

    Args:
        None

    Returns:
        DataFrame: a DataFrame of the pokemon sets
    """
    pokemon_set_dict = load_pokemon_set()
    pokemon_set_clean_df = clean_pokemon_set(pokemon_set_dict)
    return pokemon_set_clean_df


def load_pokemon_set():
    """ provides correct data path to be opened and extracted

    Args:
        file_path (str): The file location of the JSON

    Returns:
        dict: the pokemon set names, date, abr
    """
    pokemon_set_file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/' \
        f'pokemon_cards/scraped_data/pokemon_sets_2020-03-24.json'
    pokemon_set_raw = load_data(pokemon_set_file_path)
    pokemon_set_dict = pokemon_set_raw[0]
    return pokemon_set_dict


def clean_pokemon_set(pokemon_set_dict):
    """ cleans the pokemon sets by removing empty values where a japanese set
        Also fills the bottom list if a set name has been announced, but not the release date or abr name

    Args:
        pokemon_set_dict (dict): The scraped set

    Returns:
        dict: a pandas dict of the clean pokemon set
    """
    set_name = list(filter(None, pokemon_set_dict['set_name']))
    set_date = list(filter(None, pokemon_set_dict['set_date']))
    set_abr = list(filter(None, pokemon_set_dict['set_abbreviation']))

    while known_set_name_no_date(set_name, set_date):
        set_date.append('')

    while known_set_name_no_abr(set_name, set_abr):
        set_abr.append('')

    # for common name conventions between different data sets replace & with and
    set_name_clean = [name.replace('&', 'and') for name in set_name]

    pokemon_set_df = pd.DataFrame(np.array([set_name, set_date, set_abr]).T,
                                  columns=['Set Name', 'Set Date', 'Set Abr'])
    return pokemon_set_df


def known_set_name_no_date(set_name, set_date):
    return len(set_date) < len(set_name)


def known_set_name_no_abr(set_name, set_abr):
    return len(set_abr) < len(set_name)


pokemon_set_df = create_pokemon_set()



file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/pokemon_cards/scraped_data/pokemon_cards_2020-03-24.json'
df = pd.read_json(file_path)


df.dropna(subset=['Card Name'], inplace=True)
df.drop(columns=['Presale Information'], inplace=True)
df.reset_index(inplace=True)


df.loc[:, 'Stage'].unique()

# seperate by stage
not_pokemons_keys = ['Energy', 'Trainer', 'Special Energy', 'Stadium', 'Technical Machine', 'Item', '', 'Tool',
                     'Supporter']
pokemon_bool_1 = ~df['Stage'].isin(not_pokemons_keys)
pokemon_bool_2 = ~df['Stage'].isna()
pokemon_bool = pokemon_bool_1 & pokemon_bool_2
df['Is Pokemon'] = pokemon_bool




df.loc[df['Stage'] == 'bASIC', 'Stage'] = 'Basic'



# ## checking to see what makes pokemon cards unique
#
# This is how a pokemon card will be referenced later on
#
# Card name, set and number are all needed to identify a unique pokemon
# This is shown by combining the keys tags together to see if they produce a unique string equal to the total amount of pokemon



unique_id = df['Card Name'].map(str) + df['Set Name'].map(str)
pokemon_id_uniq = len(unique_id.unique())
total_cards = len(unique_id)


unique_id = df['Card Name'].map(str) + df['Card Number'].map(str)
pokemon_id_uniq = len(unique_id.unique())
total_cards = len(unique_id)


unique_id = df['Card Name'].map(str) + df['Set Name'].map(str) + df['Card Number'].map(str)
pokemon_id_uniq = len(unique_id.unique())
total_cards = len(unique_id)

df['Card Id'] = df['Card Name'].map(str) + df['Set Name'].map(str) + df['Card Number'].map(str)

pc_set = set(df['Set Name'])  # there are some weird name conventions that are going to need to be renamed
pokemon_set = set(pokemon_set_df['Set Name'])  # this the benchmark for what a set name should look like



# ## Differences in set names
# In some cases prefix like EX are added. In others Series prefix like XY or SM are deleted.
# The is no clear order and will need to be monitored when a new expansion is released


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
not_expansion




pokemon_set_table = pokemon_set_df.append(not_expansion, sort=False)
pokemon_set_table.reset_index()



pokemon_set_2 = set(pokemon_set_table['Set Name'])

# ### combining data: pokemon cards df and pokemon names df

# ### Getting all the pokemon in the pokemon cards
# filter by stage name and put a is pokemon check
# filter by if name is in a pokedex. If it is not empty put a is pokemon2 check

pokemon_teams = []
generic_name = pokemon_list_df['Pokemon Name'].str.lower().values  # contains full name of all pokemon
for pokemon_name in df['Card Name'].values:
    pokemon_team = []
    pokemon_name_clean = re.sub(r'(\(.*\))', '',
                                pokemon_name)  # removes the (filler card info) out of cards that may have unrelated pokemon in it
    pokemon_name_clean_list = pokemon_name_clean.lower().split(' ')

    pokemon_team = set()
    for ele1, ele2 in zip_longest(pokemon_name_clean_list[:], pokemon_name_clean_list[1:]):
        if ele1 in generic_name:  # a string returns true in a list if exact match. so mr.is not in a list with ['mr. mime']
            pokemon_team.add(ele1)
        if ele2 in generic_name:
            pokemon_team.add(ele2)
        if str(ele1) + ' ' + str(
                ele2) in generic_name:  # this deals with mr. mime/ mime jr. and other pokemon with multiple words
            pokemon_team.add(str(ele1) + ' ' + str(ele2))
    pokemon_teams.append(pokemon_team)


temp = pd.DataFrame(pokemon_teams, columns=['Pokemon 1', 'Pokemon 2', 'Pokemon 3'])
temp.fillna(value=np.nan, inplace=True)

df = pd.concat([df, temp], axis=1)


not_pokemon = df['Is Pokemon'] == False
has_pokemon = ~df['Pokemon 1'].isna()
bool_combined = has_pokemon & not_pokemon


# list of cards to drop from the pokemon 1
# they are cards that are not a pokemon but have a pokemon card in their name



df.loc[bool_combined, ['Pokemon 1']] = np.nan




is_pokemon = df['Is Pokemon'] == True
has_pokemon = df['Pokemon 1'].isna()
bool_combined = is_pokemon & has_pokemon



df.loc[bool_combined, ['Is Pokemon']] = False


pokemon_list_df['Pokedex Id'] = pd.Series(np.arange(1, len(pokemon_list_df) + 1, dtype='int'))


pokemon_list_df['Pokemon Name'] = pokemon_list_df['Pokemon Name'].str.lower()


keys = pokemon_list_df['Pokemon Name'].to_list()
values = pokemon_list_df['Pokedex Id'].to_list()
pokemon_number_mapping = dict(zip(keys, values))

df['Pokedex 1'] = df['Pokemon 1'].map(pokemon_number_mapping)
df['Pokedex 2'] = df['Pokemon 2'].map(pokemon_number_mapping)
df['Pokedex 3'] = df['Pokemon 3'].map(pokemon_number_mapping)


file_path = 'C:/Users/jonny/programming_content/pokemon_cards/data/snapshot_2020-03-24_test_script.csv'
df.to_csv(file_path)


