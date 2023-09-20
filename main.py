import taipy as tp
import pandas as pd
from loanshark import LoanShark
from taipy import Config, Scope, Gui, gui
from taipy.gui import Markdown
from sharksfromzip import gather_sharks
import math
import real_bank_main
import pyautogui

# Real bank lists
banks = real_bank_main.getBanks()
real_bank_names = []
real_bank_rates = []

for b in banks:
    real_bank_names.append(b.getName())
    real_bank_rates.append(b.getRate())

table = pd.DataFrame({
    'Names':real_bank_names,
    'Rates':real_bank_rates
})

# Initialization of variables
zip_code = None
zip_feedback = ""

# currently selected loan data.
selected_name = 'Enter a zip code first!'
rate = '-'
rate_output = '-'
url = '-'
stars = '-'
image = None
global shark_names_all, shark_names, shark_names_valid, shark_rates, shark_lats, shark_longs
shark_names_all = []
shark_names = []
shark_names_valid = []
shark_rates = []
shark_lats = []
shark_longs = []

# run the app

def refresh_vars():
    shark_names_all.clear()
    shark_names.clear()
    shark_names_valid.clear()
    shark_rates.clear()
    shark_lats.clear()
    shark_longs.clear()
    # populate parallel lists
    for s in sharks:
        # unique names
        if shark_names.count(s.getName()) == 0:
            shark_names.append(s.getName())

        # checks if Rate exists AND the Company is Unique.
        if float(s.getRate()) > 0 and shark_names_valid.count(s.getName()) == 0:
            shark_rates.append(float(s.getRate()))
            shark_names_valid.append(s.getName())

        # adds lats and longitudes - doesn't care about dupes.
        shark_lats.append(float(s.getLat()))
        shark_longs.append(float(s.getLong()))
        # makes a list of every name (including dupes!)
        shark_names_all.append(s.getName())
    print("1)", shark_names_valid)
    print("rates", shark_rates)
    print("valid names", shark_names_valid)

    global df
    df = pd.DataFrame({
        'Names': shark_names_valid,
        'Rates': shark_rates
    })

    print(df)

    global df_location
    df_location = (pd.DataFrame({
        'Name': shark_names_all,
        'Latitude': shark_lats,
        'Longitude': shark_longs
    }))

    print(df_location)

    global marker_map
    marker_map = {"color": "#000000", "size": 8}

    global layout_map
    layout_map = {
        "dragmode": "zoom",
        "mapbox": {"style": "open-street-map",
                   "center": {"lat": shark_lats[0], "lon": shark_longs[0]}, "zoom": 11}
    }

def submit_zip(state):
    print("Submitting or something...")
    global sharks
    sharks = gather_sharks(str(zip_code))
    refresh_vars()
    state.shark_names_valid = shark_names_valid
    state.df = df
    state.df_location = df_location
    state.shark_names = shark_names



def check_zip(state):
    global zip_code
    zip_code = state.zip_code
    try:
        zip_code = int(zip_code)

        if zip_code < 10000 or zip_code > 99999:
            state.zip_feedback = "Invalid input."
        else:
            gui.notify(state, 'I', "Processing, please wait!")
            state.zip_feedback = "Good job!"
            print("Submitting or something...")
            global sharks
            sharks = gather_sharks(str(zip_code))
            refresh_vars()
            state.shark_names_valid = shark_names_valid
            state.df = df
            state.df_location = df_location
            state.shark_names = shark_names
            global layout_map
            state.layout_map = {
                "dragmode": "zoom",
                "mapbox": {"style": "open-street-map",
                           "center": {"lat": shark_lats[0], "lon": shark_longs[0]}, "zoom": 11}
            }
            pyautogui.press('f5')


    except:
        state.zip_feedback = "Invalid input."

# Updates website info when a Company is selected
def update_info(state):
    index = shark_names.index(state.selected_name)
    state.url = sharks[index].getLink()

    if float(sharks[index].getRate()) < 0:
        state.rate_output = "No information found, try visiting their website!"
    else:
        state.rate_output = sharks[index].getRate()

    state.stars = math.floor(sharks[index].getStars())

    state.image = sharks[index].getPhotoReference()
    print("IMAGE", state.image)


global loan_main_page
loan_main_page = Markdown("""
# **You're not aLoan!**
<|layout|columns=2 2 2|color=#04003d|

<|

<|part|class_name=infobox
<h1>Real Bank Rates:</h1>

<|{table}|table|show_all|>
|>
|>


<|

<|part|class_name=infobox|
# Zip Code:
<|{zip_code}|input|on_change=check_zip|class_name=inputs|width=500px|>
|>

<|part|class_name=infobox|
# Nearby Payday Loans:
<|{selected_name}|selector|lov={shark_names}|on_change=update_info|dropdown|class_name=inputs|width=500px|>
|>

<|part|class_name=infobox|
# Map:
<|{df_location}|chart|type=scattermapbox|lat=Latitude|lon=Longitude|text=Name|marker={marker_map}|layout={layout_map}|mode=markers|height=800px|rebuild|>
|>


|>

<|
<|part|class_name=infobox|
# Payday Loan Info:
## Company Name:<|{selected_name}|>
## Interest Rate (%): <|{rate_output}|>
## More Information: <|{url}|>
## Star Rating: <|{(stars) * "⭐"}|>
|>
<|part|class_name=infobox|
<|{df}|chart|type=bar|x=Names|y=Rates|title=Various Payday Loan Rates|color=#058ed9|rebuild|>

|>

|>
|>
""")
global sharks
sharks = gather_sharks('34119')
refresh_vars()
Gui(loan_main_page).run(dark_mode=False)


