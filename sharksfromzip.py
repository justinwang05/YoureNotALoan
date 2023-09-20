
import requests, json
import webscraper
import time
import loanshark

"""
Aggregates local payday loan vendors and finds average interest rates if possible

PARAMETERS
zip(int): zipcode of user

RETURN
[loanShark]: list containing info on local payday vendors
"""
def gather_sharks(zip):
    # enter your api key here
    api_key = ''

    # variable for google place api
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    # query is passed into google place api to gather local payday loans
    query = str(zip) + " zip code payday loan"

    # response hold response of initial query (gets list of payday loaners)
    response = requests.get(url + 'query=' + query +
                     '&key=' + api_key)

    # list of local businesses place data
    businesses = response.json()['results']

    # Google details api url
    url = "https://maps.googleapis.com/maps/api/place/details/json?"

    # Sharks stores all loanShark variables
    sharks = []

    for place in businesses:
        try:
            # Google details request, gets website info of businesses gathered
            query  = place['place_id']
            response = requests.get(url + 'place_id=' + query +
                             '&key=' + api_key)
            detail = response.json()

            # Get url of payday loan vendor website and use webscraper.find() to check if they have posted interest rates
            payday_url = detail['result']['website']
            loan_rate = webscraper.find_rates(payday_url)

            # photo_ref is a photo_reference to a google place Photo object
            photo_ref = detail['result']['photos'][1]['photo_reference']

            # name stores payday loaner business name
            name = detail['result']['name']

            # star_rating stores star rating of payday loaner
            star_rating = detail['result']['rating']

            # latitude and longitude store coordinates of payday loaner
            latitude = detail['result']['geometry']['location']['lat']
            longitude = detail['result']['geometry']['location']['lng']

            sharks.append(loanshark.LoanShark(name, loan_rate , star_rating, payday_url, latitude, longitude, photo_ref))

        except Exception as error:
            2+2
    return sharks

if __name__ == "__main__":
    sharks = gather_sharks('10001')
    print(len(sharks))
    for fish in sharks:
        print(fish.name)
        print(fish.rate)
        print(fish.stars)
        print(fish.link)
        print()
