![bulbasaur](https://assets.pokemon.com/assets/cms2/img/cards/web/EX4/EX4_EN_39.png)
![charmander](https://assets.pokemon.com/assets/cms2/img/cards/web/SMA/SMA_EN_SV6.png)
![squirtle](https://assets.pokemon.com/assets/cms2/img/cards/web/BW7/BW7_EN_29.png)  
Which is the cutest? 
Source: https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/

# Data Engineering Project:

## Using ETL process to create a Pokemon Card database with card stats and daily prices

This pokemon project main purpose is for me to learn and demonstrate key data engineering(DE) tools and techniques for creating a data pipeline. Along the way, I borrow concepts from 'Designing Data-Intensive Applications' to create a reliable, scalable and maintainable system. This md file helps to document my journey and break down the project into several stages.  

Im glad to be contributing a new dataset for data analyst/scientist who love pokemon!


## Table of contents guide:

Each **intro** contains:
1. Identiying the problems
2. Defining the goals

Each **conclusion** contains:
1. Future problems
2. Resources used


## Table of contents
1. [**Project Details**](#Project_Details)
    - Project descripion  
    - Intro  
    - Technologies  
2. [**Data Extracting**](#Data_Extracting)
    - Intro
    - Webscraping
    - Conclusion
3. [**Data Staging Transformation**](#Data_Staging_Transformation)
    - Intro
    - Creating A Data Snapshot
    - Conclusion
4. [**Data Normalziation Transformation**](#Data_Normalization_Transformation)
5. [**Data Warehouse**](#Data_Warehouse)
6. [**Database Design**](#Database_Design)
7. [**Data Loading**](#Data_Loading)
10.[**Self-Notes/Resources**](#Self-Notes/Resources)

# 1. Project Details <a id='Project_Details'></a>
## Project descripion


This projects focuses on a common data engineering task known as **Extract, Transform and Load (ETL)**. 

#### Project outline

1. Project Details: overview of project and more 
2. Data Extracting: how data is gathered from a varity of sources
3. Data Staging Transformation: how the data is gathered and stored as a single daily snapshot sheet
4. Data Normalization Transformation: How the data is broken down and cleaned for data loading
5. Data Warehouse: how the Data Warehouse is created and organized
6. Database Design: how to normalize the data and create the tables
7. Data Loading: How the data base is updated
10. Other side notes


## Intro

#### Creating a pokemon cards database with the daily prices:

First of all, I am doign this project because I wanted to create a data engineering portfolio showcasing my ETL process using key technologies on a trendy topic that is interesting to me, provides some value, and is easy to understand. Right now, there currently is no way to analyze pokemon card prices over time which I intend to solve!


## Basic info

To understanding the challenges of creating a pokemon card database, first some basic questions need to be asked to understand the projects contex.

##### What is a pokemon card?  
The pokemon Trading Card Game is a collectible card game, based on Nintendo's Pokémon franchise of video games and anime, first published in October 1996 by Media Factory in Japan. There are many types of pokemon cards such as items, energy, trainers and of course pokemon. This project is narrowing the scope to only pokemon cards that are pokemon.

![example](<https://assets.pokemon.com/assets/cms2/img/cards/web/SMA/SMA_EN_SV6.png>)

##### What are you collecting from the pokemon cards?  
The pokemon in the cards each have a name, a type, and an amount of Health Points (HP). Additionaly many of them have attacks with names, type, damage amount and cost amount. Furthermore, there are extra stat like weakness, resistance, retreat cost, rarity and a pokemon number that many of them have. 

##### Where would your data come from?  
There are sites that host pokemon card data such as  
https://www.pokemon.com/us/pokemon-tcg/pokemon-cards/   
https://pokemontcg.io/   
https://pkmncards.com/   

- TCGplayer is the main site that sells pokemon cards and they have their own API for a current sales price of a card  
https://shop.tcgplayer.com/pokemon  

##### what sales price data can you gain access with tcgplayer API?  
https://help.tcgplayer.com/hc/en-us/articles/201577976-How-can-I-get-access-to-your-card-pricing-data-
They can only provide access to cards of the current date. You can get access to low/mid/high pricing. This can be see on pkmncards.com. Tcg player site however has its own version with a market/median price and foil market/median price.


##### Does evey pokemon card have a price?  
No. Some cards are tournament winning cards for example and are rarely placed on the market.
 
 
##### Have similar projects been done before? What makes your project unique? Why does your project matter?  
There are websites that host pokemon cards stats and display current price. However, there are none that show the price over time of a given card. This means you can not compare pokemon cards based off their price with much certainty. Also, when an expansion is introduced, new cards can have powerful synergies with older cards causing their prices to change. Having the associated price with cards can lead to better understanding of what makes a card desirable.

##### What will your final result look like? 
1. To create an accessible data base that can be queried
2. To create a csv form to share to kaggle, a popular data hub for data scientists.


## Technologies Used

**Data Gathering:**
- Scrapy (webscraping framework built)

**Processing:**
- Pandas (data manipulation tool)

**Storage:**
- JSON (key value object storage)
- S3 (HDFS storage)


**Automation**
- Air Flow (lets me run the ETL job daily at the same time daily)

**Version Control**
- Git 


# 2. Data Extracting <a id='Data_Extracting'></a>

    - Intro
    - Webscraping
        - pc_bulk
        - pokemon_sets
        - pokemon_list
        - pc_meta_data
    - Conclusion
## Identiying the problems 

Currently, TCG player has data on the pokemon card stats and prices. Their API will require constant renewal and only provides low, medium and high prices. On their site, they show a more detailed description showing a cards market/median price and foil market/median price. The API also does not return details on the pokemon cards. Therefore, a webscraper will be used to gently carry out this task.

When webscraping, you should look at the websites robot.txt file. In this case, they allow webscraping but wish there to be a crawl delay of 10 seconds which anyone webscraping would ignore since it's so high. I will use Autothrottle, since 10 seconds is not practical, but I do not wish to over load their servers.

Scrapy docs describe autothrottling as:  
A way to automatically throttling crawling speed based on load of both the Scrapy server and the website you are crawling.  
Its design goals where to  
1. be nicer to sites instead of using default download delay of zero  
2. automatically adjust Scrapy to the optimum crawling speed, so the user doesn’t have to tune the download delays to find the optimum one. The user only needs to specify the maximum concurrent requests it allows, and the extension does the rest.

https://shop.tcgplayer.com/robots.txt  
**robots.txt**
User-agent: *  
Crawl-Delay: 10  
Disallow: /admin/  
Disallow: /checkout/  
Disallow: /myaccount/  
Disallow: /*?*xid=  
Allow: /  


## Defining the goals
    
There will be a couple webscrapers that scrape from different sources.

Scrapy is my personal choice for webscraping. It is described from the docs as:
'Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.'  
https://github.com/scrapy/scrapy/blob/2.0/docs/index.rst

The webscrapers created are shown in the table below:


| Scraper ID | Scraper Name | Source      |  Output Description          | 
|------------|-------------:|:-----------:|-----------------------------:|
| 1          | pokemon_cards|  tcgplayer  |  bulk stats w/ prices        |
| 2          | pokemon_sets |  Bulbapedia |  list of expansions w/ dates |
| 3          | pokemon_list |  Bulbapedia |  list of pokemon w/ pokdex # | 

#### File format

Each output file is in JSON and is the scraper name followed by the current data.  
Example: pc_meta_data_2020_03_01.json


#### pokemon_cards sample output:  
"Card Name": "Charmander",  
"Set Name": "Arceus",  
"Card Number": "59",  
"Rarity": "Common",   
"Card Type": "Fire",  
"HP": "60",  
"Stage": "Basic",  
"Attack 1": "[1] Call for Friends - Search your deck for a R Basic Pokemon, show it to your opponent, and put it into your hand.  Shuffle your deck afterward."   
"Attack 2": "[1R] Steady Firebreathing (20)",  
"Weakness": "W+10",  
"Retreat Cost": "",  
"Market Price Normal": "$0.59",  
"Market Price Foil": "N/A",  
"Median Price Normal": "$0.53",  
"Median Price Foil": "N/A",  
"Url": "https://shop.tcgplayer.com/pokemon/arceus/charmander",  
"Scraped Date": "2020-03-01",   


![charmander](https://6d4be195623157e28848-7697ece4918e0a73861de0eb37d08968.ssl.cf1.rackcdn.com/84217_200w.jpg)  



## Future problems
## Resources used

https://github.com/scrapy/scrapy/blob/2.0/docs/index.rst
https://docs.scrapy.org/en/latest/index.html  
https://docs.scrapy.org/en/latest/topics/autothrottle.html  
https://shop.tcgplayer.com/robots.txt


# 3. Data Staging Transformation <a id='Data_Staging_Transformation'></a>

The data is recieved as a JSON file and is transformed through Pythons' Pandas library. A large dataframe is created that wrangles the data and formats it as a single dataframe or snapshot. 


<img src=https://pandas.pydata.org/docs/_static/pandas.svg width="200" align="left" >   
  
'pandas is a Python package providing fast, flexible, and expressive data structures designed to make working with "relational" or "labeled" data both easy and intuitive. It aims to be the fundamental high-level building block for doing practical, real world data analysis in Python. Additionally, it has the broader goal of becoming the most powerful and flexible open source data analysis / manipulation tool available in any language.' - docs  
https://github.com/pandas-dev/pandas/blob/master/README.md





# 5. Database Design <a id='Database_Design'></a>

1. creating a entity relationship diagram
2. grouping data in the table format
3. collecting type metrics for data types
4. creating tables
5. setting constraints
6. creating updates functions

Store data in the format you will access it.

Data Warehouse:  
- Store snapshot of a given day
- Create a Table of a Card ID, Date Scaped, Prices, item amount
- Create a Table of a Card ID, all the stats updated not normalized
- Create a Table that updates the card stats by taking source data from card


## Goals

#### Self-goals:
- To learn data engineering key concepts, technologies and best practices
- To demonstrait my skill/workflow to future employers (aka get a job)
- To creat a novel pokemon cards database with stats and daily prices

#### Sharing-goals:
- To share my project experience on Medium, GIT and other data engineering communities
    - this is a **data engineering project** 
- To contribute to the pokemon data analyst/scientist communities such as kaggle
    - this is for **data analyst/scientist**


