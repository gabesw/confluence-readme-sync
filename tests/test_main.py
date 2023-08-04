import os
import unittest
from unittest.mock import patch, mock_open
from main import main
from src.errors import InvalidParameterError, ConfluenceApiError, SubstringNotFoundError
from markdown import markdown

@patch('src.utils.extract_domain_and_page_id')
@patch('src.api.ConfluenceClient.send')
@patch('src.api.GetPageCommand')
@patch('src.api.GetPageCommandInput')
@patch('src.api.EditPageCommand')
@patch('src.api.EditPageCommandInput')
@patch('markdown.markdown')
class TestMain(unittest.TestCase):
    @patch.dict(os.environ, {
        "INPUT_FILEPATH": "gabesw.md",
        "INPUT_URL": "https://domain/wiki/spaces/aSpace/pages/1234567890/Gabesw",
        "INPUT_TOKEN": "aksh74HLKF7hiu78P1VSKAB7",
        "INPUT_USERNAME": "gabesw@example.com",
        "INPUT_INSERT_START_TEXT": "<p>start</p>",
        "INPUT_INSERT_END_TEXT": "<p>end</p>"
    })
    def test_main_success(self, mock_markdown, mock_edit_page_command_input, mock_edit_page_command, mock_get_page_command_input, mock_get_page_command, mock_confluence_client_send, mock_extract_domain_and_page_id):
        mock_extract_domain_and_page_id.return_value = ("domain", "1234567890")
        get_page_text = """
        {
            "status": 200,
            "title": "Some Title",
            "body": {
                "storage": {
                    "value": "<p>start</p><p>end</p>"
                }
            },
            "version": {
                "number": 1
            }
        }
        """
        mock_get_page_response = type('Response', (), {'text': get_page_text, 'status_code': 200})
        mock_edit_page_response = type('Response', (), {'raise_for_status': lambda : None, 'status_code': 200})
        mock_confluence_client_send.side_effect = [mock_get_page_response, mock_edit_page_response]
        mock_markdown.return_value = "<h1>hi</h1>"
        with self.assertLogs(level='INFO') as cm:
            with patch('builtins.open', mock_open(read_data='#hi')) as open:
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
    def test_main_bad_env_vars(self, mock_markdown, mock_edit_page_command_input, mock_edit_page_command, mock_get_page_command_input, mock_get_page_command, mock_confluence_client_send, mock_extract_domain_and_page_id):
        with self.assertLogs(level='INFO') as cm:
            with self.assertRaises(InvalidParameterError):
               main()
        self.assertEqual(cm.output, [
           'INFO:root:Starting README sync...',
        ])
#TODO: add tests for ConfluenceApiError and SubstringNotFoundError