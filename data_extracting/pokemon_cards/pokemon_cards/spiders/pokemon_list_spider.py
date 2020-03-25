import scrapy
from scrapy.loader import ItemLoader
from pokemon_cards.items import PokemonList


class PokemonListSpider(scrapy.Spider):
    # this scraper collects all the pokemon list in order
    name = 'pokemon_list'

    def start_requests(self):
        # This starts the web scraper at the correct website
        url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
        yield scrapy.Request(url=url, callback=self.parse_pokemon_list)

    def parse_pokemon_list(self, response):
        # this collects all pokemon names
        pokemon_list_raw = response.xpath("//tr[@style ='background:#FFF']/td/a/text()").getall()
        pokemon_list = list(dict.fromkeys(pokemon_list_raw))
        loader = ItemLoader(PokemonList(), response)
        loader.add_value('pokemon_list', pokemon_list)
        yield loader.load_item()
