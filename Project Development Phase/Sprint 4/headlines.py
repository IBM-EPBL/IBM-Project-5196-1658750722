from newsapi import NewsApiClient
import pycountry

def news_category(country,category):
    # you have to get your api key from newapi.com and then paste it below
    newsapi = NewsApiClient(api_key='')

    # now we will take name of country from user as input
    input_country = country
    input_countries = [f'{input_country.strip()}']
    countries = {}


    # iterate over all the countries in
    # the world using pycountry module
    for country in pycountry.countries:

	    # and store the unique code of each country
	    # in the dictionary along with it's full name
	    countries[country.name] = country.alpha_2

    # now we will check that the entered country name is
    # valid or invalid using the unique code
    codes = [countries.get(country.title(), 'Unknown code')
		    for country in input_countries]

    # now we have to display all the categories from which user will
    # decide and enter the name of that category
    option = category

    # now we will fetch the new according to the choice of the user
    top_headlines = newsapi.get_top_headlines(

	    # getting top headlines from all the news channels
	    category=f'{option.lower()}', language='en', country=f'{codes[0].lower()}')

    # fetch the top news under that category
    Headlines = top_headlines['articles']
    title=[]
    url=[]
    urltoimage=[]




    # now we will display the that news with a good readability for user
    if Headlines:
		    for articles in Headlines:
			    b = articles['title'][::-1].index("-")
			    if "news" in (articles['title'][-b+1:]).lower():
				    title.append(f"{articles['title']}")
				    url.append(f"{articles['url']}")
				    urltoimage.append(f"{articles['urlToImage']}")
				

			    else:
				    title.append(f"{articles['title']}")
				    url.append(f"{articles['url']}")
				    urltoimage.append(f"{articles['urlToImage']}")
		    return title,url,urltoimage

    else:
	    print(f"Sorry no articles found for {input_country}, Something Wrong!!!")
	    option = input("Do you want to search again[Yes/No]?")


def news_headlines(country):
	# you have to get your api key from newapi.com and then paste it below
	newsapi = NewsApiClient(api_key='')

	# now we will take name of country from user as input
	input_country = country
	input_countries = [f'{input_country.strip()}']
	countries = {}

	# iterate over all the countries in
	# the world using pycountry module
	for country in pycountry.countries:
		# and store the unique code of each country
		# in the dictionary along with it's full name
		countries[country.name] = country.alpha_2

	# now we will check that the entered country name is
	# valid or invalid using the unique code
	codes = [countries.get(country.title(), 'Unknown code')
			 for country in input_countries]

	# now we have to display all the categories from which user will
	# decide and enter the name of that category


	# now we will fetch the new according to the choice of the user
	top_headlines = newsapi.get_top_headlines(

		# getting top headlines from all the news channels
		 language='en', country=f'{codes[0].lower()}')

	# fetch the top news under that category
	Headlines = top_headlines['articles']
	title = []
	url = []
	urltoimage = []

	# now we will display the that news with a good readability for user
	if Headlines:
		for articles in Headlines:
			b = articles['title'][::-1].index("-")
			if "news" in (articles['title'][-b + 1:]).lower():
				title.append(f"{articles['title']}")
				url.append(f"{articles['url']}")
				urltoimage.append(f"{articles['urlToImage']}")


			else:
				title.append(f"{articles['title']}")
				url.append(f"{articles['url']}")
				urltoimage.append(f"{articles['urlToImage']}")
		return title, url, urltoimage

	else:
		print(f"Sorry no articles found for {input_country}, Something Wrong!!!")
		option = input("Do you want to search again[Yes/No]?")







