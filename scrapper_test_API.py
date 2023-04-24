from scrapper import Olx_Scrapper, OtoDom_Scrapper
import json
import os
import time

SAVE_PATH = "results"
MAX_SCRAPPING_TRY = 5
CITY = "katowice"


def TEST_API(city: str):
    json_dict = []
    fail = {"Description": "Failed",
            "Total price": "Failed",
            "Price": "Failed",
            "Rent": "Failed",
            "Area": "Failed",
            "Rooms": "Failed",
            "Deposit": "Failed",
            "Floor": "Failed",
            "Type": "Failed",
            "Status": "Failed"
            }

    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    with open(f"{SAVE_PATH}/crawler_result_{city}.json", 'r') as f:
        crawler_data = json.load(f)

    scrapper_olx = Olx_Scrapper()
    scrapper_otoDom = OtoDom_Scrapper()

    num_of_links = len(crawler_data)
    json_dict = crawler_data

    for i, record in enumerate(crawler_data):
        print("                                      ", end='\r')
        print(f"Scrapped {i + 1}/{num_of_links} links", end="\r")
        link = record['Link']
        if "olx" in link:
            for j in range(MAX_SCRAPPING_TRY):
                try:
                    json_dict[i].update(scrapper_olx.run(link))
                except:
                    json_dict[i].update(fail)
                else:
                    break
        elif "otodom" in link:
            for j in range(MAX_SCRAPPING_TRY):
                try:
                    json_dict[i].update(scrapper_otoDom.run(link))
                except:
                    json_dict[i].update(fail)
                else:
                    break

    with open(f'{SAVE_PATH}/scrapper_result_{city}.json', 'w', encoding='utf8') as f:
        json.dump(json_dict, f, indent=4, ensure_ascii=False)


while True:
    TEST_API('katowice')
    time.sleep(3600)
