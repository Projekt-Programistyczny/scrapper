import unittest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from src.scrapper import Scrapper_Base, OtoDom_Scrapper, Olx_Scrapper

class TestScrapper(unittest.TestCase):
    def setUp(self):
        self.otodom_scrapper = OtoDom_Scrapper()
        self.olx_scrapper = Olx_Scrapper()

    def test_otodom_get_details(self):
        soup = self.otodom_scrapper._get_page('https://www.otodom.pl/pl/oferta/bedzin-podskarpie-nowy-apartament-69mkw-do-wynaj-ID4ls8b')

        expected_output = {
            'description': 'Będzin Podskarpie nowy apartament 69mkw do wynaj.', 
            'total_price': 4700.0, 
            'price': 4500.0, 
            'rent': 200.0, 
            'currency': 'zł', 
            'area': 69.0, 
            'rooms': 3.0, 
            'deposit': 11000.0, 
            'floor': '1/2', 
            'type': 'apartamentowiec', 
            'status': 'do zamieszkania', 
            'region': 'śląskie'
        }

        result = self.otodom_scrapper._get_details(soup)

        self.assertEqual(result, expected_output)

    def test_olx_get_details(self):
        soup = self.olx_scrapper._get_page('https://www.olx.pl/d/oferta/mieszkanie-2-pokojowe-bedzin-centrum-po-remoncie-CID3-IDN8K44.html')

        expected_output = {
            'description': 'Mieszkanie 2 pokojowe BĘDZIN centrum po REMONCIE!', 
            'total_price': 1840.0, 
            'price': 1390.0, 
            'rent': 450.0, 
            'currency': 'zł', 
            'area': 40.0, 
            'rooms': 2.0, 
            'deposit': -1.0, 
            'floor': 'Parter', 
            'type': 'Blok', 
            'status': 'Umeblowane', 
            'region': 'śląskie'
        }

        result = self.olx_scrapper._get_details(soup)

        self.assertEqual(result, expected_output)

    def test_clean_str_to_num(self):
        input_str = "123,45 zł"
        expected_output = 123.45
        result = self.otodom_scrapper._clean_str(input_str, True, "zł")
        self.assertEqual(result, expected_output)

    def test_clean_str_to_str(self):
        input_str = "Powierzchnia: 100 m²"
        expected_output = "100"
        result = self.otodom_scrapper._clean_str(input_str, False, "Powierzchnia:", "m²")
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
