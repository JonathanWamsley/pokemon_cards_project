import scrapy
from scrapy.loader import ItemLoader
from pokemon_cards.items import PokemonSet


class PokemonSetsSpider(scrapy.Spider):
    # this spider collects the set name, release date and set abbreviation
    name = 'pokemon_sets'

    def start_requests(self):
        # This starts the web scraper at the correct website
        url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_Trading_Card_Game_expansions"
        yield scrapy.Request(url=url, callback=self.parse_pokemon_sets)

    def parse_pokemon_sets(self, response):
        # this collects all set info in the table using xpath and stores them in the item loader
        set_name = response.xpath("//tr[1]//td[ 4]/a/text()").getall()
        set_date = response.xpath("//tr[1]//td[ 8]/text()").getall()
        set_date = [str(d).strip() for d in set_date]
        set_abbreviation = response.xpath("//tr[1]//td[ 10]/text()").getall()
        set_abbreviation = [str(s).strip() for s in set_abbreviation]
        loader = ItemLoader(PokemonSet(), response)
        loader.add_value('set_name', set_name)
        loader.add_value('set_date', set_date)
        loader.add_value('set_abbreviation', set_abbreviation)
        yield loader.load_item()
