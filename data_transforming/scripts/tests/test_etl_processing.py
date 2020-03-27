import unittest
import pandas as pd
import numpy as np
import json
import re
from itertools import zip_longest
from datetime import date

from pandas.testing import assert_frame_equal, assert_series_equal

from snapshot_transformation.etl_processing import (create_pokemon_set, load_data, clean_pokemon_list)


class TestETLProcessing(unittest.TestCase):
    def test_load_data(self):
        test_pokemon_list_path  = 'C:/Users/jonny/programming_content/pokemon_cards/data_transforming/scripts/tests/' \
                            'test_data/test_pokemon_list.json'
        with open(test_pokemon_list_path) as f:
            raw_data = json.load(f)

        expected = [{'pokemon_list': ['Bulbasaur', 'Ivysaur', 'Venusaur']}]
        self.assertEqual(raw_data, expected)


if __name__ == "__main__":
    unittest.main()
