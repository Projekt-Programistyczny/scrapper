import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
from src.scrapper import OtoDom_Scrapper, Olx_Scrapper

class TestScrapper(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.mock_session.get.return_value.text = ""
        self.mock_soup = BeautifulSoup("", "html.parser")
    
    @patch("scrapper.Session")
    def test_init_session(self, mock_session):
        scrapper = OtoDom_Scrapper()
        self.assertEqual(scrapper.session, self.mock_session)
    
    @patch("scrapper.Session")
    def test_get_page(self, mock_session):
        scrapper = OtoDom_Scrapper()
        soup = scrapper._get_page("https://example.com")
        self.assertEqual(soup, self.mock_soup)
    
    def test_clean_str_to_num(self):
        scrapper = OtoDom_Scrapper()
        str_input = "10,000.50 zł"
        result = scrapper._clean_str(str_input, True, "zł")
        self.assertEqual(result, 10000.50)
    
    def test_clean_str_to_str(self):
        scrapper = OtoDom_Scrapper()
        str_input = "Example text 123"
        result = scrapper._clean_str(str_input, False, "text")
        self.assertEqual(result, "Example 123")
    
    def test_oto_dom_get_details(self):
        scrapper = OtoDom_Scrapper()
        self.mock_soup.find_all = MagicMock(return_value=["Example Title", "10,000.50 zł", "100 m²", "3 pokoje"])
        result = scrapper._get_details(self.mock_soup)
        self.assertEqual(result["description"], "Example Title")
        self.assertEqual(result["total_price"], 10000.50)
        self.assertEqual(result["currency"], "zł")
        self.assertEqual(result["area"], 100)
        self.assertEqual(result["rooms"], 3)
    
    def test_olx_get_details(self):
        scrapper = Olx_Scrapper()
        self.mock_soup.find_all = MagicMock(return_value=["Example Title", "10,000.50 zł", "100 m²", "3 pokoje"])
        result = scrapper._get_details(self.mock_soup)
        self.assertEqual(result["description"], "Example Title")
        self.assertEqual(result["total_price"], 10000.50)
        self.assertEqual(result["currency"], "zł")
        self.assertEqual(result["area"], 100)
        self.assertEqual(result["rooms"], 3)

if __name__ == "__main__":
    unittest.main()