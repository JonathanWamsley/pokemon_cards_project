import scrapy
from datetime import date
import re


class PokemonCardsSpider(scrapy.Spider):
    # this scraper collects all the pokemon card stats and prices
    name = "pokemon_cards"

    def start_requests(self):
        # This starts the web scraper at
        url = "https://shop.tcgplayer.com/price-guide/pokemon"
        yield scrapy.Request(url=url, callback=self.parse_pokemon_sets)

    def parse_pokemon_sets(self, response):
        # This collects all the pokemon sets for indexing the pages where the pokemon cards are at
        pokemon_sets = response.xpath("//select[2][@class='priceGuideDropDown']/option/text()").getall()
        for pokemon_set in pokemon_sets:
            # the url is cleaned for proper url access
            pokemon_set = pokemon_set.replace(' - ', '-')
            pokemon_set = pokemon_set.replace('&', 'and')
            pokemon_set = pokemon_set.replace("'s", 's')
            pokemon_set = pokemon_set.replace(":", '')
            pokemon_set = pokemon_set.replace(')', '')
            pokemon_set = pokemon_set.replace('(', '')
            pokemon_set = pokemon_set.replace(' ', '-')
            url = 'https://shop.tcgplayer.com/price-guide/pokemon/' + str(pokemon_set)
            yield scrapy.Request(url=url, callback=self.parse_pokemon_cards)

    def parse_pokemon_cards(self, response):
        # this page jumps into all the pokemon cards with a link that leads to where all the desired data is at
        pokemon_stats_links = response.xpath("//div[@class='productDetail']/a/@href").getall()
        for pokemon_stats_link in pokemon_stats_links:
            next_url = response.urljoin(pokemon_stats_link)
            yield scrapy.Request(url=next_url, callback=self.parse_pokemon_stats)

    def parse_pokemon_stats(self, response):
        data = {}  # stores info in a dictionary and not item loader since the info names can vary
        pokemon_name = response.xpath("//h1[@class='product-details__name']/text()").get()
        pokemon_set = response.xpath("//div[@class='product-details__set']/a/text()").get()
        data['Card Name'] = pokemon_name
        data['Set Name'] = pokemon_set

        # Gathers all the product info. For each term there is a corresponding description with varying formats
        product_terms = response.xpath("//dt")
        product_descriptions = response.xpath("//dd")

        for product_term, product_description in zip(product_terms, product_descriptions):
            terms = str(product_term.getall())
            terms = re.sub("(\<.*?\>)", "", terms)
            terms = terms.replace("['", '').replace("']", '').replace("\\'", "'").replace("\\r\\n", '').replace(':', '')
            term = (''.join(terms).split('/'))

            descriptions = str(product_description.getall())
            descriptions = re.sub("(\<.*?\>)", "", descriptions)
            descriptions = descriptions.replace("['", '').replace("']", '').replace("\\'", "'").replace("\\r\\n", '')
            description = descriptions.split(' / ')

            # now the terms and descriptions are cleaned and can be mapped out
            for t, d in zip(term, description):
                data[t.strip()] = d.strip()

        # Gathers the price info
        price_names = response.xpath("//th[@class='price-point__name']")
        price_values = response.xpath("//td[@class='price-point__data']")
        # this mapping has the possible ways the data can be displayed
        # there can be 3 non empty configurations. 2 non foils, 2 foils, or both 2 non foils and 2 foils
        if len(price_names) == 2:
            mapping = {'Market Price ': 1, 'Median Price ': 2}  # Either Normal or Foil will be appended
        else:
            mapping = {'Market Price Normal': 1, 'Market Price Foil': 2,
                       'Median Price Normal': 3, 'Median Price Foil': 4}
        index = 1  # keeps track of mapping index value
        for price_name, price_value in zip(price_names, price_values):
            name = price_name.xpath("./text()").getall()
            value = price_value.xpath("./text()").getall()

            for k, v in mapping.items():
                if v == index:  # forces mark price first index 1 to be mapped, then index 2 at median price
                    if len(price_names) == 2:
                        full_name = k + ''.join(name)
                        data[full_name] = ''.join(value)
                    else:  # if len is not 2 it is 4 and has a set mapping of names
                        data[k] = ''.join(value)
            index += 1
        data['Url'] = response.request.url
        data['Scraped Date'] = date.today()
        yield data

