import unittest
import pandas as pd
import numpy as np
import json
import re
from itertools import zip_longest
from datetime import date

from pandas.testing import assert_frame_equal, assert_series_equal

from snapshot_transformation.etl_processing import (load_data, clean_pokemon_set)


class TestETLProcessing(unittest.TestCase):
    def test_load_data(self):
        test_pokemon_list_path  = 'C:/Users/jonny/programming_content/pokemon_cards/data_transforming/scripts/tests/' \
                            'test_data/test_pokemon_list.json'
        expected_data = [{'pokemon_list': ['Bulbasaur', 'Ivysaur', 'Venusaur']}]
        data = load_data(test_pokemon_list_path)
        self.assertEqual(data, expected_data)

    def test_clean_pokemon_set(self):
        pass



if __name__ == "__main__":
    unittest.main()
