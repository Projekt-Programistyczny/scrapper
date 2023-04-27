from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util import Retry
from abc import ABC, abstractmethod
from typing import Dict, Union
from tenacity import retry
from tenacity.wait import wait_exponential
import bs4


"""
Author: Kamil Wieczorek
Contact: vieczorkamil@gmail.com
Version: 0.2
Date: 24-04-2023
"""


class Scrapper_Base(ABC):
    def __init__(self, session_retry_connect: int=15,
                       session_retry_read: int=15,
                       session_retry_redirect: int=15) -> None:
        
        self.session_retry_connect = session_retry_connect
        self.session_retry_read = session_retry_read
        self.session_retry_redirect = session_retry_redirect
        self.page_limit = 150

        self.session = self._init_session()


    def run(self, url: str) -> Dict:
        soup = self._get_page(url)
        return self._get_details(soup)


    @abstractmethod
    def _get_details(self, soup: bs4.BeautifulSoup) -> Dict:
        pass


    def _init_session(self) -> Session:
        session = Session()
        retries = Retry(connect=self.session_retry_connect,
                        read=self.session_retry_read,
                        redirect=self.session_retry_redirect)

        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))

        return session
    

    @retry(wait=wait_exponential(multiplier=1, min=2, max=5))
    def _get_page(self, url) -> bs4.BeautifulSoup:
        with self.session as s:
            page_source = s.get(url=url)
            soup = bs4.BeautifulSoup(page_source.text, "html.parser")

        return soup
    

    def _clean_str(self, str_input: str, to_num: bool, *str_to_delete: str) -> Union[str, float]:
        str_output = str_input.replace(" ", "")
        for arg in str_to_delete:
            str_output = str_output.replace(arg, "")
        if to_num:
            if str_output == "Zapytaj":
                return 0
            elif str_output == "Kawalerka":
                return 1
            else:
                str_output = str_output.replace(",", ".")
                return float(str_output)
        else:
            return str_output


class OtoDom_Scrapper(Scrapper_Base):
    def __init__(self, session_retry_connect: int = 15, 
                       session_retry_read: int = 15, 
                       session_retry_redirect: int = 15) -> None:
        super().__init__(session_retry_connect, session_retry_read, session_retry_redirect)

    
    def _get_details(self, soup: bs4.BeautifulSoup) -> Dict:
        title = soup.find_all("h1", class_="css-1wnihf5 efcnut38")[0].text

        price = soup.find_all("strong", class_="css-1i5yyw0 e1l1avn10")[0].text

        if "zł" in price.lower():
            currency = "zł"
        elif "eur" in price.lower():
            currency = "eur"
        elif "usd" in price.lower():
            currency = "usd"
        else:
            currency = "Brak info"

        price = self._clean_str(price, True, "zł", "ZŁ", "EUR", "eur", "USD", "usd")

        description = soup.find_all("div", class_="css-1qzszy5 enb64yk1")

        area = description[1].text #co dwa
        area = self._clean_str(area, True, "m²")

        rent = description[3].text
        rent = self._clean_str(rent, True, "zł/miesiąc", "ZŁ/miesiąc", "eur/miesiąc", "EUR/miesiąc")

        rooms = description[5].text
        rooms = self._clean_str(rooms, True, "więcejniż") #TODO: handle "więcej niż"

        deposit = description[7].text
        deposit = self._clean_str(deposit, True, "zł", "eur", "usd", "ZŁ", "EUR", "USD")

        floor = description[9].text
        type_of_floor = description[11].text
        status = description[19].text

        region = soup.find_all("a", class_="css-1in5nid e19r3rnf1")[1].text

        ret = {"Description": title,
               "Total price": price+rent,
               "Price": price,
               "Rent": rent,
               "Currency": currency,
               "Area": area,
               "Rooms": rooms,
               "Deposit": deposit,
               "Floor": floor,
               "Type": type_of_floor,
               "Status": status,
               "Region": region
               }
        
        return ret
    
    
class Olx_Scrapper(Scrapper_Base):
    def __init__(self, session_retry_connect: int = 15, 
                       session_retry_read: int = 15, 
                       session_retry_redirect: int = 15) -> None:
        super().__init__(session_retry_connect, session_retry_read, session_retry_redirect)

    
    def _get_details(self, soup: bs4.BeautifulSoup) -> Dict:
        title = soup.find_all("h1", class_="css-1soizd2 er34gjf0")[0].text

        price = soup.find_all("h3", class_="css-ddweki er34gjf0")[0].text

        if "zł" in price.lower():
            currency = "zł"
        elif "eur" in price.lower(): #TODO: check
            currency = "eur"
        elif "usd" in price.lower():
            currency = "usd"
        else:
            currency = "Brak info"

        price = self._clean_str(price, True, "zł")

        description_temp = soup.find_all("ul", class_="css-sfcl1s")[0]

        description = []
        for i in description_temp:
            description.append(i.text)

        # init values as "Brak info"

        area = "Brak info"
        rent = 0
        rooms = "Brak info"
        deposit = "Brak info"
        floor = "Brak info"
        type_of_floor = "Brak info"
        status = "Brak info"
        region = "Brak info"
        
        for i in description[1:]:
            if "Powierzchnia" in i:
                area = self._clean_str(i, True, "Powierzchnia:", "m²")
            elif "Czynsz" in i:
                rent = self._clean_str(i, True, "Czynsz(dodatkowo):", "zł")
            elif "Liczba pokoi" in i:
                rooms = self._clean_str(i, True, "Liczbapokoi:", "pokoje", "iwięcej") # TODO: handle "4 i więcej"
            elif "Poziom" in i:
                floor = self._clean_str(i, False, "Poziom:")
            elif "Rodzaj zabudowy:" in i:
                type_of_floor = self._clean_str(i, False, "Rodzajzabudowy:")
            elif "Umeblowane:" in i:
                status = self._clean_str(i, False, "Umeblowane:")
                if status == "Tak": status = "Umeblowane" 
                else: status = "Brak umeblowania"

        try:
            region = soup.find_all("a", class_="css-tyi2d1")[4].text.split()[-1].lower()
        except:
            region = "Brak info"


        ret = {"Description": title,
               "Total price": price+rent,
               "Price": price,
               "Rent": rent,
               "Currency": currency,
               "Area": area,
               "Rooms": rooms,
               "Deposit": deposit,
               "Floor": floor,
               "Type": type_of_floor,
               "Status": status,
               "Region": region
               }
        
        return ret
