import requests
from bs4 import BeautifulSoup


"""
Shortens url to only primary address, allows for easier reading of pages by program

PARAMETERS
url(String): url being cut

RETURN
String: shortened url
"""
def cut_url(url):
    counter = 0
    for i in range(0,len(url)):
        if(url[i] == "/"):
            counter += 1
        if(counter == 3):
            return url[0:i+1]

"""
given index of a percentage sign, finds the rest of the percentage based on html source

PARAMETERS
response(String): HTML source of website

index(int): Index of percentage sign in response

RETURN
String: complete percent preceding the percentage sign, -1 if the percentage sign is not preceded by numbers
"""
def find_full_percent(response,index):
    i = index
    percent = ""
    while True:
        if(response[i] == "."):
            percent += "."
            i -= 1
        else:
            try:
                percent+= str(int(response[i]))
                i -= 1
            except:
                break
    if percent == "":
        return -1
    else:
        return  percent[::-1]


"""
Attempts to find the interest rate posted on a payday loan vendor's website

PARAMETERS
url(String): url of payday loan vendor website

RETURN
float: interest rate posted on loan vendors website, -1 if no interest rate is found
"""
def find_rates(url):
    # prepares url to be read and searched through
    url = cut_url(url)

    # stores keywords to look for, program will search pages that include these keywords
    keywords = ['rate','apr']

    # stores source of vendor website
    response = requests.get(url)

    #parse source into <a> tags, since these contain links to pages with interest information
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.find_all('a')

    # if no percent is found, interest rate is -1
    percent = -1

    #search through all <a> tags
    for a in names:

        # try each keyword in each <a> tag
        for key in keywords:

            # check if the keyword appears in the tag, if so check the linked page
            if key in str(a).lower():

                # get source of linked page
                rate_url = str(a.get('href'))
                rate_response = requests.get(url[0:len(url) - 1] + rate_url).text

                #while loop checks linked page source for percents,
                while True:

                    #checks if a percent has been found
                    has_percentage = False
                    for j in range (0,10):
                        index = rate_response.find(str(j) + '%')
                        if( index != -1):
                            has_percentage = True
                            break

                    # if a percent has been found, see if it is the largest available and make sure it is over 100
                    # (interest rates on payday loans are not lower than 100%, and percentages lower than this often are html related)
                    if has_percentage:
                        possible_percent = find_full_percent(rate_response,index)
                        if float(percent) < float(possible_percent) and float(possible_percent) > 100:
                            percent = find_full_percent(rate_response, index)

                        # cut response body where the percent was found, and look for more in the body
                        rate_response = rate_response[index+1:]
                    else:
                        break
    return percent


if __name__ == "__main__":
    out = find_rates('https://fastpaydayloansfloridainc.com/')
    print(out)