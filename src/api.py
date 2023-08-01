from abc import ABC, abstractmethod
import json
import requests
from requests import Response
from requests.auth import HTTPBasicAuth

class CommandInput(ABC):
    """
    The abstract base class for all command inputs.
    """

    @abstractmethod
    def __init__(self, domain: str):
        """
        Initialize the base command input with a domain.

        :param domain: The domain of the API to interact with.
        """
        self.domain = domain


class GetPageCommandInput(CommandInput):
    """
    Concrete implementation of CommandInput for the :class:`GetPageCommand` class.
    """
    
    def __init__(self, domain: str, page_id: str):
        """
        Initialize the command input with a domain and a page ID.

        :param domain: The domain of the API to interact with.
        :param page_id: The ID of the page to retrieve.
        """
        super().__init__(domain)
        self.id = page_id


class EditPageCommandInput(CommandInput):
    """
    Concrete implementation of CommandInput for the :class:`EditPageCommand` class.
    """
    
    def __init__(self, domain: str, page_id: str, page_status: str, page_title: str, page_body: str, version_number: int):
        """
        Initialize the command input with domain, page ID, page status, page title, page body, and version number.

        :param domain: The domain of the API to interact with.
        :param page_id: The ID of the page to edit.
        :param page_status: The status of the page to set.
        :param page_title: The title of the page to set.
        :param page_body: The body content of the page to set.
        :param version_number: The current version number of the page.
        """
        super().__init__(domain)
        self.id = page_id
        self.status = page_status
        self.title = page_title
        self.body = page_body
        self.version = version_number + 1


class ApiCommand(ABC):
    """
    The abstract base class for all API commands. 
    This class plays the role of the Command in the Command pattern.
    """
    
    @abstractmethod
    def __init__(self, input: CommandInput):
        """
        Initialize the base command with a command input.

        :param input: The command input to use.
        """
        self.input = input
    
    @abstractmethod
    def execute(self, auth: HTTPBasicAuth) -> Response:
        """
        Abstract method for executing the command, to be implemented in subclasses.

        :param auth: The HTTPBasicAuth to use for authentication.
        :return: The response from the API.
        """
        pass


class GetPageCommand(ApiCommand):
    """
    Concrete implementation of ApiCommand for getting a page.
    This class plays the role of a Concrete Command in the Command pattern.
    """
    
    def __init__(self, input: GetPageCommandInput):
        """
        Initialize the command with a GetPageCommandInput.

        :param input: The command input to use.
        """
        super().__init__(input)
        self.input = input
    
    def execute(self, auth: HTTPBasicAuth) -> Response:
        """
        Execute the command by sending a GET request to the API.

        :param auth: The HTTPBasicAuth to use for authentication.
        :return: The response from the API.
        """
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
    """
    Concrete implementation of ApiCommand for editing a page.
    This class plays the role of a Concrete Command in the Command pattern.
    """
    
    def __init__(self, input: EditPageCommandInput):
        """
        Initialize the command with an EditPageCommandInput.

        :param input: The command input to use.
        """
        super().__init__(input)
        self.input = input
    
    def execute(self, auth: HTTPBasicAuth) -> Response:
        """
        Execute the command by sending a PUT request to the API.

        :param auth: The HTTPBasicAuth to use for authentication.
        :return: The response from the API.
        """
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
        })

        return requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers,
            auth=auth
        )


class ConfluenceClient:
    """
    Client class for interacting with the API. 
    This class plays the role of the Invoker in the Command pattern.
    """
    
    def __init__(self, auth: HTTPBasicAuth):
        """
        Initialize the client with an HTTPBasicAuth object.

        :param auth: The HTTPBasicAuth to use for authentication.
        """
        self.auth = auth
    
    def send(self, command: ApiCommand):
        """
        Send a command to the API and return the response.

        :param command: The command to execute.
        :return: The response from the API.
        """
        return command.execute(self.auth)