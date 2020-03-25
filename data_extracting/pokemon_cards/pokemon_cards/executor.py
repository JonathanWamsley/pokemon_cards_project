import os
'''
    This script spawns a new process for each job to run. 
    This is done because when you run a scrapy job the script it terminated after single use.
'''

if __name__ == "__main__":
    jobs = ['pokemon_sets', 'pokemon_list', 'pokemon_cards']
    for job in jobs:
        os.system(f'python runner.py {job}')

