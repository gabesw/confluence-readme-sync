import json
from os import environ
import re
from typing import Dict
from utils import extract_domain_and_page_id
from api import ConfluenceClient, GetPageCommand, GetPageCommandInput, EditPageCommand, EditPageCommandInput
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import markdown
from confluence_markdown_extension import ConfluenceExtension

load_dotenv()

def main():
    # retrieve and verify env variables
    vars: Dict[str, str] = {}
    for key in ["filepath", "url", "username", "token", "insert_start_text", "insert_end_text"]:
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
    
    # read markdown file
    md_text: str
    with open(vars["filepath"], 'r') as f:
        md_text = f.read()

    # convert markdown file to html
    converted_html = markdown.markdown(md_text, extensions=['tables', ConfluenceExtension()])

    # insert markdown between insert_start_text and insert_end_text
    start_substring: str = vars["insert_start_text"]
    end_substring: str = vars["insert_end_text"]
    start_index = page_body.find(start_substring)
    end_index = page_body.find(end_substring)
    if start_index == -1 or end_index == -1 or start_index > end_index: raise LookupError("Insert after string was not found in the body of the Confluence page")
    page_body = page_body[:start_index + len(start_substring)] + converted_html + page_body[end_index:end_index + len(end_substring)] + page_body[end_index + len(end_substring):]

    # create edit page command
    input = EditPageCommandInput(domain, page_id, page_status, page_title, page_body, page_version_number)
    command = EditPageCommand(input)

    response = client.send(command)
    print("Success!") #DEBUG

if __name__ == "__main__":
    main()