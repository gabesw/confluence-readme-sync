import unittest
from src.api import *
from unittest.mock import patch
from requests import Response
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth("username", "password")

class TestGetPageCommandInput(unittest.TestCase):
    def test_init(self):
        domain = "example.com"
        id = "1234567890"
        input = GetPageCommandInput(domain, id)
        self.assertEqual(input.domain, domain, "Domain value should be equal to the domain parameter")
        self.assertEqual(input.id, id, "ID value should be equal to the ID parameter")

class TestEditPageCommandInput(unittest.TestCase):
    def test_init(self):
        domain = "example.com"
        id = "1234567890"
        status = "new"
        title = "Title"
        body = "<p>body</p>"
        version = 1
        input = EditPageCommandInput(domain, id, status, title, body, version)
        self.assertEqual(input.domain, domain, "Domain value should be equal to the domain parameter")
        self.assertEqual(input.id, id, "ID value should be equal to the ID parameter")
        self.assertEqual(input.status, status, "Status value should be equal to the status parameter")
        self.assertEqual(input.title, title, "Title value should be equal to the title parameter")
        self.assertEqual(input.body, body, "Body value should be equal to the body parameter")
        self.assertEqual(input.version, version+1, "Version value should be equal to the version parameter incremented by 1")

class TestGetPageCommand(unittest.TestCase):
    def setUp(self):
        domain = "example.com"
        id = "1234567890"
        self.input = GetPageCommandInput(domain, id)
        self.command = GetPageCommand(self.input)
    def test_init(self):
        self.assertEqual(self.command.input, self.input, "Command input should be a GetPageCommandInput")
    @patch('requests.request')
    def test_execute(self, mock_request):
        response = self.command.execute(auth)
        self.assertIsNotNone(response)
        mock_request.assert_called_with(
            "GET",
            f"https://{self.input.domain}/wiki/api/v2/pages/{self.input.id}",
            headers = {"Accept": "application/json"},
            auth = auth,
            params = {"body-format": "storage"}
        )

class TestEditPageCommand(unittest.TestCase):
    def setUp(self):
        domain = "example.com"
        id = "1234567890"
        status = "new"
        title = "Title"
        body = "<p>body</p>"
        version = 1
        self.input = EditPageCommandInput(domain, id, status, title, body, version)
        self.command =EditPageCommand(self.input)
    def test_init(self):
        self.assertEqual(self.command.input, self.input, "Command input should be an EditPageCommandInput")
    @patch('requests.request')
    def test_execute(self, mock_request):
        response = self.command.execute(auth)
        self.assertIsNotNone(response)
        page = self.input
        payload = json.dumps( {
        "id": page.id,
        "status": page.status,
        "title": page.title,
        "body": {
            "representation": "storage",
            "value": page.body
        },
        "version": {
            "number": page.version,
            "message": "Page updated automatically by confluence-readme-sync GitHub action"
        }
        })
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        mock_request.assert_called_with(
            "PUT",
            f"https://{self.input.domain}/wiki/api/v2/pages/{self.input.id}",
            data = payload,
            headers = headers,
            auth = auth,
        )

class TestConfluenceClient(unittest.TestCase):
    def setUp(self):
        self.client = ConfluenceClient(auth)
    def test_init(self):
        self.assertEqual(self.client.auth, auth)
    def test_send(self):
        class FakeCommandInput(CommandInput):
            def __init__(self, domain: str):
                super().__init__(domain)
        class FakeCommand(ApiCommand):
            def __init__(self, input: FakeCommandInput):
                super().__init__(input)
            def execute(self, auth: HTTPBasicAuth) -> Response:
                return Response()
        input = FakeCommandInput("example.com")
        command = FakeCommand(input)
        response = self.client.send(command)
        self.assertIsInstance(response, Response)