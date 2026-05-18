import os

import requests
from urllib.request import urlopen
import json
from dotenv import load_dotenv
api_url = 'https://api.calorieninjas.com/v1/nutrition?query='

load_dotenv("key.env")
with open('all_produce.json') as f:
    d = json.load(f)
    
for i in d:
    if "name_en" in i:  
        
        query = i["name_en"]
        response = requests.get(api_url + query, headers={'X-Api-Key': os.getenv("api_key")})
        response2 = response.json()["items"]
        
        for item in response2:
            item.pop("name", None)
       
        i["nutrients"] = response2

        if response.status_code == requests.codes.ok:
            print("OK")
        else:
            print("Error:", response.status_code, response.text)
        
        with open('all_produce.json', 'w') as f:
            json.dump(d, f, indent=4)

