import unittest
from src.utils import *
from unittest.mock import patch

url = "https://example.atlassian.net/wiki/spaces/teamSE/pages/1234567890/Page+Name"

class TestExtractDomainFromUrl(unittest.TestCase):
    def test_success(self):
        domain: str = extract_domain_from_url(url)
        self.assertEqual(domain, "example.atlassian.net", "Should extract domain from valid URL")
    def test_fail(self):
        with self.assertRaises(ValueError, msg="Invalid URL should raise a ValueError"):
            extract_domain_from_url("")

class TestExtractPageIdFromUrl(unittest.TestCase):
    def test_success(self):
        id: str = extract_page_id_from_url(url)
        self.assertEqual(id, "1234567890", "Should extract id from valid URL")
    def test_fail(self):
        with self.assertRaises(ValueError, msg="Invalid URL should raise a ValueError"):
            extract_page_id_from_url("")

@patch('src.utils.extract_domain_from_url')
@patch('src.utils.extract_page_id_from_url')
class TestExtractDomainAndPageIdFromUrl(unittest.TestCase):
    def test_success(self, mock_extract_page_id_from_url, mock_extract_domain_from_url):
        domain = "example.atlassian.net"
        id = "1234567890"
        mock_extract_page_id_from_url.return_value = id
        mock_extract_domain_from_url.return_value = domain
        result = extract_domain_and_page_id(url)
        self.assertTupleEqual((domain, id), result)

if __name__ == '__main__':
    unittest.main()