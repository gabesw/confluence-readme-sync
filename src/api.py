from abc import ABC, abstractmethod
import json
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

class EditPageCommandInput(CommandInput):
    def __init__(self, domain: str, page_id: str, page_status: str, page_title: str, page_body: str, version_number: int):
        super().__init__(domain)
        self.id = page_id
        self.status = page_status
        self.title = page_title
        self.body = page_body
        self.version = version_number + 1

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
    
class EditPageCommand(ApiCommand):
    def __init__(self, input: EditPageCommandInput):
        super().__init__(input)
        self.input = input
    def execute(self, auth: HTTPBasicAuth) -> Response:
        page = self.input

        url = f"https://{self.input.domain}/wiki/api/v2/pages/{self.input.id}"

        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

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
        } )

        return requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )

class ConfluenceClient:
    def __init__(self, auth: HTTPBasicAuth):
        self.auth = auth
    def send(self, command: ApiCommand):
        return command.execute(self.auth)