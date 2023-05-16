from src.scrapper import Olx_Scrapper, OtoDom_Scrapper
from src.database import *
import json
import os
import time

SCRAPPER_INTERVAL = 5 * 60 # 5 minutes
MAX_SCRAPPING_TRY = 5
CITY_TO_EXPLORE = ['katowice']
DEBUG = True


def run_scrapper(city: str):
    list_of_scrapped_data = []
    scrapped_data_failed = {"description": "Failed",
                            "total price": "Failed",
                            "price": "Failed",
                            "rent": "Failed",
                            "area": "Failed",
                            "rooms": "Failed",
                            "deposit": "Failed",
                            "floor": "Failed",
                            "type": "Failed",
                            "status": "Failed"
                            }

    crawler_data = select_unused_and_active_links(city)
    scrapper_olx = Olx_Scrapper()
    scrapper_otoDom = OtoDom_Scrapper()
    num_of_links = len(crawler_data)

    index = 0


    for i, record in enumerate(crawler_data):
        print("                                      ", end='\r')
        print(f"Scrapped {i + 1}/{num_of_links} links", end="\r")

        link = record.url
        list_of_scrapped_data.append({"url": link})

        if "olx" in link:
            for j in range(MAX_SCRAPPING_TRY):
                try:
                    list_of_scrapped_data[index].update(scrapper_olx.run(link))
                except:
                    list_of_scrapped_data[index].update(scrapped_data_failed)
                else:
                    break
        elif "otodom" in link:
            for j in range(MAX_SCRAPPING_TRY):
                try:
                    list_of_scrapped_data[index].update(scrapper_otoDom.run(link))
                except:
                    list_of_scrapped_data[index].update(scrapped_data_failed)
                else:
                    break
        set_link_as_used(link)
        index += 1

        # optimize memory -> save data in chunk
        # also connection cannot be open such long time 
        if (i % 250 == 0):
            add_offers(list_of_scrapped_data)
            list_of_scrapped_data = []
            index = 0

    # save the rest of data 
    add_offers(list_of_scrapped_data)
    

if __name__ == "__main__":
    if not DEBUG:
        while True:
            for city in CITY_TO_EXPLORE:
                run_scrapper(city)
            time.sleep(SCRAPPER_INTERVAL)
    else:
        for city in CITY_TO_EXPLORE:
            run_scrapper(city)