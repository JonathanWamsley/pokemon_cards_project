# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PokemonList(scrapy.Item):
    pokemon_list = scrapy.Field()


class PokemonSet(scrapy.Item):
    set_name = scrapy.Field()
    set_date = scrapy.Field()
    set_abbreviation = scrapy.Field()
