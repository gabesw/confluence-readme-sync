from abc import ABC, abstractmethod
import requests
from requests import Response
from requests.auth import HTTPBasicAuth

class CommandInput(ABC):
    @abstractmethod
    def __init__(self, domain: str):
        self.domain = domain

class GetPageCommandInput(CommandInput):
    def __init__(self, domain: str, page_id: str):
        super().__init__(domain)
        self.id = page_id

class ApiCommand(ABC):
    @abstractmethod
    def __init__(self, input: CommandInput):
        self.input = input
    @abstractmethod
    def execute(self, auth: HTTPBasicAuth) -> Response:
        pass

class GetPageCommand(ApiCommand):
    def __init__(self, input: GetPageCommandInput):
        super().__init__(input)
        self.input = input
    def execute(self, auth: HTTPBasicAuth) -> Response:
        url = f"https://{self.input.domain}/wiki/api/v2/pages/{self.input.id}"
        headers = {
        "Accept": "application/json"
        }
        query = {
            "body-format": "storage"
        }
        return requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth,
            params=query
        )

class ConfluenceClient:
    def __init__(self, auth: HTTPBasicAuth):
        self.auth = auth
    def send(self, command: ApiCommand):
        return command.execute(self.auth)