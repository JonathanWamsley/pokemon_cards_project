#!/usr/bin/env python
# coding: utf-8

# # Pokemon Card snapshot transformation
#
# #### *This notebook is used to protype data processing before it is implement into a .py script.*
# - Notebooks are good for protoyping, i.e. getting things to work quickly and being able to visualize dataframe changes in code snippets
# - Notebooks are bad for production, i.e. abstracting complexities, unit testing, maintaining, monitoring code
#
# Previously, I scraped data from [bulbapedia (pokemon list data)](https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number), [bulbapedia (pokemon sets data)](https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_Trading_Card_Game_expansions) and [tcgplayer (pokemon card data)](https://shop.tcgplayer.com/price-guide/pokemon). From these 3 sites I generated json files that contain the following:
#
#  - **pokemon_list.json**
#      - pokemon generic name - like in the pokedex that is already ordered
#  - **pokemon_sets.json**
#      - pokemon set name
#      - pokemon set release date
#      - pokemon set abbreviation
#  - **pokemon_stats_date_scraped.json**
#      - card name
#      - card set
#      - card number
#      - card rarity
#      - card type
#      - pokemon HP
#      - pokemon evolution stage
#      - card median price
#      - card foil median price
#      - card market price
#      - card foil market price
#      - pokemon resistance
#      - pokemon weakness
#      - pokemon attack [1,2,3,4]
#      - card text
#      - web scraped date
#      - card url
#
#     - created columns
#          - pokemon [1,2,3]
#          - pokedex [1,2,3]
#          - card id (surgate of card name, set and number)
#          - set date
#          - set abr
#
# #### This notebook shows how data is imported and processed(combined, clearned and other common data wrangling tasks) to be saved as a single snapshot (this will be saved in an S3 bucket)

# ## Importing required libraries

# In[1]:


import pandas as pd
import numpy as np
import json
import re
import os
from itertools import zip_longest
from datetime import date

# ## 1) processing the pokemon_list
#     The pokedex is a list of every unique pokemon
#
# #### **Cleaning guide:**
# 3 pokemon names were altered because they used special characters unlike the tcgplayer website
#
# * Note that the pokedex is already in order

# In[2]:


file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/pokemon_cards/scraped_data/pokemon_list_2020-03-24.json'
with open(file_path) as f:
    raw_data = json.load(f)
pokemon_list = raw_data[0]['pokemon_list']
pokemon_list[28] = 'Nidoran F'
pokemon_list[31] = 'Nidoran M'
pokemon_list[668] = 'Flabebe'

pokemon_list_df = pd.DataFrame(data=pokemon_list, columns=['Pokemon Name'])
pokemon_list_df.head()

# ## 2) processing pokemon_sets
#     contains the following:
#
#     Set name: official expansion name
#     Set date: When set was released
#     Set abr: Abbreviation of the set name
#
# #### **Cleaning guide:**
# - There were 2 sets that were released in japan but no in English. blank lines were created and therefore removed
# - The set name had '&' changed to 'and' to follow the format from tcg player sets
# - A filler element is appended if the newest pokemon set name is known but the release date or abr is not

# In[3]:


file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/pokemon_cards/scraped_data/pokemon_sets_2020-03-24.json'
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

pokemon_set_df = pd.DataFrame(np.array([set_name, set_date, set_abr]).T, columns=['Set Name', 'Set Date', 'Set Abr'])
pokemon_set_df['Set Name'] = pokemon_set_df['Set Name'].str.replace('&', 'and')
pokemon_set_df.tail()

# ## 3) pokemon card stats
#
# Contains the folllowing parameters:
#  - card surogate id (name, number, set)
#  - card name
#  - card number
#  - card rarity
#  - card type
#  - card HP
#  - card evolution stage
#  - card median price
#  - card foil median price
#  - card market price
#  - card foil market price
#  - card resistance
#  - card weakness
#  - card attack [1,2,3,4]
#  - card text
#  - web scraped date
#  - card url
#
#
# #### **Cleaning guide:**
#
# - Loading Data
# - Adding a Card ID tag

# In[96]:


file_path = f'C:/Users/jonny/programming_content/pokemon_cards/data_extracting/pokemon_cards/pokemon_cards/scraped_data/pokemon_cards_2020-03-24.json'
df = pd.read_json(file_path)
df.head(2)

# ### Checking NA values for all pokemon cards
# - shows Card Name, a Set Name and a Rarity are all filled
# - card number is mostly filled

# In[97]:


df.dropna(subset=['Card Name'], inplace=True)
df.drop(columns=['Presale Information'], inplace=True)
df.reset_index(inplace=True)

# In[98]:


df.isna().sum()

# ### all the unique pokemon stage names
# This is useful since stage name can divide pokemon and non pokemon categories

# In[99]:


df.loc[:, 'Stage'].unique()

# In[100]:


# seperate by stage
not_pokemons_keys = ['Energy', 'Trainer', 'Special Energy', 'Stadium', 'Technical Machine', 'Item', '', 'Tool',
                     'Supporter']
pokemon_bool_1 = ~df['Stage'].isin(not_pokemons_keys)
pokemon_bool_2 = ~df['Stage'].isna()
pokemon_bool = pokemon_bool_1 & pokemon_bool_2
df['Is Pokemon'] = pokemon_bool

# ### Minor cleaning
# There are more errors to come. Most won't be addressed in this notebook. But for now, to get the right key values.
# A future project that ensures data integrity by:
# - scrapes pokemon card images
# - uses aws rekognition to extract the text
# -  update the data base with correct values

# In[101]:


df.loc[df['Stage'] == 'bASIC', ['Card Name', 'Set Name', 'Stage']]

# In[102]:


df.loc[df['Stage'] == 'bASIC', 'Stage'] = 'Basic'

# In[103]:


df.loc[df['Is Pokemon'] == True, :]['Stage'].unique()

# ## checking to see what makes pokemon cards unique
#
# This is how a pokemon card will be referenced later on
#
# Card name, set and number are all needed to identify a unique pokemon
# This is shown by combining the keys tags together to see if they produce a unique string equal to the total amount of pokemon

# In[104]:


df.isna().sum()

# In[105]:


unique_id = df['Card Name'].map(str) + df['Set Name'].map(str)
pokemon_id_uniq = len(unique_id.unique())
total_cards = len(unique_id)
print(f'There are a total of {total_cards} pokemon and combining card name and set name there are {pokemon_id_uniq}')

# In[106]:


unique_id = df['Card Name'].map(str) + df['Card Number'].map(str)
pokemon_id_uniq = len(unique_id.unique())
total_cards = len(unique_id)
print(f'There are a total of {total_cards} pokemon and combining card name and card number there are {pokemon_id_uniq}')

# In[107]:


unique_id = df['Card Name'].map(str) + df['Set Name'].map(str) + df['Card Number'].map(str)
pokemon_id_uniq = len(unique_id.unique())
total_cards = len(unique_id)
print(
    f'There are a total of {total_cards} pokemon and combining card name, set name and card number there are {pokemon_id_uniq}')

# In[108]:


df['Card Id'] = df['Card Name'].map(str) + df['Set Name'].map(str) + df['Card Number'].map(str)

# ### Combining data: pokemon cards df and set names df

# In[109]:


pc_set = set(df['Set Name'])  # there are some weird name conventions that are going to need to be renamed
pokemon_set = set(pokemon_set_df['Set Name'])  # this the benchmark for what a set name should look like

# In[110]:


print(f'There are {len(pokemon_set - pc_set)} missing or mislabeled sets in the pokemon set df and not from tcgplayer')

# In[111]:


print(f'There are {len(pc_set - pokemon_set)} missing or mislabeled sets in the pokemon set df and not from tcgplayer')

# ## Differences in set names
# In some cases prefix like EX are added. In others Series prefix like XY or SM are deleted.
# The is no clear order and will need to be monitored when a new expansion is released

# In[112]:


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
pokemon_set - pc_set  # should be empty or is the latest set that name has been announced, but not the pokemon cards

# In[113]:


print(f'There are {len(pokemon_set - pc_set)} missing sets in the pokemon set df and not from tcgplayer')

# In[114]:


not_expansion = pd.DataFrame(list(pc_set - pokemon_set), columns=[
    'Set Name'])  # investigating this sets show that they are promotion, tournament winning cards, error cards
not_expansion

# In[115]:


pokemon_set_table = pokemon_set_df.append(not_expansion, sort=False)
pokemon_set_table.reset_index()

# In[116]:


pokemon_set_2 = set(pokemon_set_table['Set Name'])
print(
    f'There are {len(pc_set - pokemon_set_2)} missing or mislabeled sets in the pokemon set df and not from tcgplayer')

# ### combining data: pokemon cards df and pokemon names df

# ### Getting all the pokemon in the pokemon cards
# filter by stage name and put a is pokemon check
# filter by if name is in a pokedex. If it is not empty put a is pokemon2 check
#

# In[117]:


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

# In[118]:


temp = pd.DataFrame(pokemon_teams, columns=['Pokemon 1', 'Pokemon 2', 'Pokemon 3'])
temp.fillna(value=np.nan, inplace=True)

# In[123]:


df = pd.concat([df, temp], axis=1)

# In[124]:


df.head(3)

# In[125]:


not_pokemon = df['Is Pokemon'] == False
has_pokemon = ~df['Pokemon 1'].isna()
bool_combined = has_pokemon & not_pokemon

# In[127]:


# list of cards to drop from the pokemon 1
# they are cards that are not a pokemon but have a pokemon card in their name
df[bool_combined]

# In[128]:


df.loc[bool_combined, ['Pokemon 1']] = np.nan

# In[129]:


is_pokemon = df['Is Pokemon'] == True
has_pokemon = df['Pokemon 1'].isna()
bool_combined = is_pokemon & has_pokemon

# In[132]:


df[bool_combined]

# In[134]:


df.loc[bool_combined, ['Is Pokemon']] = False

# ## Give each pokemon a pokedex value

# In[135]:


pokemon_list_df['Pokedex Id'] = pd.Series(np.arange(1, len(pokemon_list_df) + 1, dtype='int'))

# In[136]:


pokemon_list_df['Pokemon Name'] = pokemon_list_df['Pokemon Name'].str.lower()

# In[137]:


keys = pokemon_list_df['Pokemon Name'].to_list()
values = pokemon_list_df['Pokedex Id'].to_list()
pokemon_number_mapping = dict(zip(keys, values))

# In[138]:


df['Pokedex 1'] = df['Pokemon 1'].map(pokemon_number_mapping)
df['Pokedex 2'] = df['Pokemon 2'].map(pokemon_number_mapping)
df['Pokedex 3'] = df['Pokemon 3'].map(pokemon_number_mapping)

# ### Snap shot data is complete

# In[139]:


df.head()

# In[141]:


file_path = 'C:/Users/jonny/programming_content/pokemon_cards/data/snapshot_2020-03-24_test_script.csv'
df.to_csv(file_path)

# ## Saving the snapshot to an S3 Bucket
#
# The files will be stored in a S3 bucket in the from of
# > s3://pokemon_cards_warehouse/snapshots/filename_date
#
# > S3://pokemon_cards_warehouse/card_prices
#
#
# Will store snapshot as S3 and then move to S3 Glacier after data has been processed
#

# In[36]:


import boto3

# In[ ]:


# import boto3
# s3 = boto3.client('s3')
# bucket = s3.create_bucket(Bucket='pokemon_cards_warehouse')

