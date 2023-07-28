import json
from os import environ
from typing import Dict
from utils import extract_domain_and_page_id
from api import ConfluenceClient, GetPageCommand, GetPageCommandInput, EditPageCommand, EditPageCommandInput
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

def main():
    # retrieve and verify env variables
    vars: Dict[str, str] = {}
    for key in ["filepath", "url", "username", "token", "insert_after"]:
        value = environ.get(f"INPUT_{key.upper()}")
        if not value:
            raise ValueError(f"Error: Missing value for {key}")
        vars[key] = value

    domain, page_id = extract_domain_and_page_id(vars["url"])

    # set up client
    auth = HTTPBasicAuth(vars["username"], vars["token"])
    client = ConfluenceClient(auth)

    # create get page command
    input = GetPageCommandInput(domain, page_id)
    command = GetPageCommand(input)

    response = client.send(command)
    json_response_body = json.loads(response.text)

    # process get page results
    page_status: str = json_response_body["status"]
    page_title: str = json_response_body["title"]
    page_body: str = json_response_body["body"]["storage"]["value"]
    page_version_number: int = json_response_body["version"]["number"]
    if not (page_status and page_title and page_body and page_version_number): raise ValueError("Values were not correctly received from get page")
    insert_after_string: str = vars["insert_after"]
    index = page_body.find(insert_after_string)
    if index == -1: raise LookupError("Insert after string was not found in the body of the Confluence page")
    markdown_to_insert: str = "some markdown here" #PLACEHOLDER - READ README AND CONVERT TO HTML FOR THIS
    # insert markdown after the insert_after_string
    page_body = page_body[:index + len(insert_after_string)] + markdown_to_insert + page_body[index + len(insert_after_string):]

    # create edit page command
    input = EditPageCommandInput(domain, page_id, page_status, page_title, page_body, page_version_number)
    command = EditPageCommand(input)

    response = client.send(command)

if __name__ == "__main__":
    main()