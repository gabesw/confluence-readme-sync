import json
from os import environ
from typing import Dict
from utils import extract_domain_and_page_id
from api import ConfluenceClient, GetPageCommand, GetPageCommandInput
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

def main():
    # retrieve and verify env variables
    vars: Dict[str, str] = {}
    for key in ["filepath", "url", "username", "token"]:
        value = environ.get(f"INPUT_{key.upper()}")
        if not value:
            raise ValueError(f"Error: Missing value for {key}")
        vars[key] = value

    domain, page_id = extract_domain_and_page_id(vars["url"])

    auth = HTTPBasicAuth(vars["username"], vars["token"])
    client = ConfluenceClient(auth)

    input = GetPageCommandInput(domain, page_id)
    command = GetPageCommand(input)

    response = client.send(command)
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

if __name__ == "__main__":
    main()