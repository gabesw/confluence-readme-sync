import os
import unittest
from unittest.mock import patch
from main import main
from src.errors import InvalidParameterError, ConfluenceApiError, SubstringNotFoundError

@patch('src.utils.extract_domain_and_page_id')
@patch('src.api.ConfluenceClient')
@patch('src.api.GetPageCommand')
@patch('src.api.GetPageCommandInput')
@patch('src.api.EditPageCommand')
@patch('src.api.EditPageCommandInput')
class TestMain(unittest.TestCase):
    @patch.dict(os.environ, {
        "INPUT_FILEPATH": "gabesw.md",
        "INPUT_URL": "https://domain/wiki/spaces/aSpace/pages/1234567890/Gabesw",
        "INPUT_TOKEN": "aksh74HLKF7hiu78P1VSKAB7",
        "INPUT_USERNAME": "gabesw@example.com",
        "INPUT_INSERT_START_TEXT": "<p>start</p>",
        "INPUT_INSERT_END_TEXT": "<p>end</p>"
    })
    def test_main_success(self, mock_edit_page_command_input, mock_edit_page_command, mock_get_page_command_input, mock_get_page_command, mock_confluence_client, mock_extract_domain_and_page_id):
        with self.assertLogs(level='INFO') as cm:
            main()
        self.assertEqual(cm.output, [
            'INFO:root:Starting README sync...',
            'INFO:root:Getting confluence page content.',
            'INFO:root:Reading markdown file.',
            'INFO:root:Converting markdown file.',
            'INFO:root:Updating confluence page.',
            'INFO:root:Sync successful!'
        ])
    @patch.dict(os.environ, {}, clear=True)
    def test_main_bad_env_vars(self, mock_edit_page_command_input, mock_edit_page_command, mock_get_page_command_input, mock_get_page_command, mock_confluence_client, mock_extract_domain_and_page_id):
        url = os.environ.get("INPUT_URL")
        print()
        with self.assertLogs(level='INFO') as cm:
            with self.assertRaises(InvalidParameterError):
               main()
        self.assertEqual(cm.output, [
           'INFO:root:Starting README sync...',
        ])