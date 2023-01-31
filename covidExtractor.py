import requests
import sys
import pandas as pd
from time import sleep
from random import randrange

CONFIGURL = "https://covid19map.elixir-luxembourg.org/minerva/api/configuration/"
PROJECTURL = "https://covid19map.elixir-luxembourg.org/minerva/api/projects/"

header = {  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'covid19map.elixir-luxembourg.org',
            'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.69'}



def changeCookies(cookie):
    for cook in cookie:
        cookies[cook] = cookie[cook]

print(f"getting config {CONFIGURL}")
res = requests.get(CONFIGURL, headers=header)

if res.ok:
    cookies = res.cookies.get_dict()
    config = None
    for i in res.json()["options"]:
        if i["type"] == "DEFAULT_MAP":
            config = i["value"]
            break

    else:
        print("config not found")
        sys.exit()

    PROJECTURL += (config + "/models/")

    print(f"getting models {PROJECTURL}")
    res = requests.get(PROJECTURL, headers=header, cookies=cookies)

    if res.ok:
        changeCookies(res.cookies.get_dict())
        models = res.json()

        MODELEXTACTORURL = PROJECTURL
        for model in models:
            id = str(model["idObject"])
            URL = MODELEXTACTORURL + id + "/bioEntities/elements/?columns=%20id,name,type,references"

            print(f"getting model with id {id} {URL}")

            while True:
                try:
                    response = requests.get(URL, headers=header, cookies=cookies)

                    if response.ok:
                        changeCookies(response.cookies.get_dict())
                        data = response.json()
                        df = pd.DataFrame(data)
                        df.to_excel(f"module_{id}.xlsx", index=False)
                    
                        sleep(randrange(20,35)/10)
                        break
                        

                    else:
                        print(f"error to get module {id} info retring")
                        sleep(randrange(10,30)/10)
                    
                except:
                    print(f"server error for module {id} tring again")
                    sleep(randrange(10,30)/10)
                    
    else:
        print("error to get modules file")
else:
    print("error to get config file")


    


