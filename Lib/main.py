import os
import requests
from datetime import datetime

NUT_APP_ID = os.environ.get("NUT_APP_ID")
NUT_API_KEY = os.environ.get("NUT_API_KEY")
SHEETY_PROJECT = "myWorkouts"
SHEET = "sheet1"
SHEETY_AUTH = os.environ.get("SHEETY_AUTH")

nutritionix_endpoint = "https://trackapi.nutritionix.com/"
nutritionix_post_ext = "v2/natural/exercise"

nutr_header = {
    "x-app-id": NUT_APP_ID,
    "x-app-key": NUT_API_KEY
}

nutr_post_parameters = {
    "query": "Ran for 15 minutes.",
    "gender": "male",
    "weight_kg": 84,
    "height_cm": 157,
    "age": 31
}

today = datetime.now().strftime("%m-%d-%Y")

nutr_api_call = f"{nutritionix_endpoint}{nutritionix_post_ext}"
nutr_response = requests.post(url=nutr_api_call, json=nutr_post_parameters, headers=nutr_header)
nutr_jdata = nutr_response.json()

exercise = nutr_jdata["exercises"][0]["name"].title()
duration = nutr_jdata["exercises"][0]["duration_min"]
calories = nutr_jdata["exercises"][0]["nf_calories"]

sheety_endpoint = \
    (f"https://api.sheety.co/bfcaa73edd17edb613cd16a2c54f110c/{SHEETY_PROJECT}/{SHEET}")

sheety_row_entry = {
    "sheet1": {
        "date": today,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

sheety_header = {
    "Authorization": SHEETY_AUTH
}

sheety_response = requests.post(url=sheety_endpoint, json=sheety_row_entry, headers=sheety_header)
