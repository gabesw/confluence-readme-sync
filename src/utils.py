import re

def extract_domain_and_page_id(url: str) -> tuple[str, str]:
    """
    Extracts the domain and the page ID from a Confluence page URL.

    :param str url: The url to a Confluence page, including the 'https://'
    :return tuple[str, str]: A tuple in the format of [domain, page_id]
    """
    domain = extract_domain_from_url(url)
    page_id = extract_page_id_from_url(url)
    return domain, page_id

def extract_domain_from_url(url: str) -> str:
    """
    Extracts the domain from a Confluence page URL.

    :param str url: The url to a Confluence page, including the 'https://'
    :return str: The domain of the url
    """
    # Match the domain between https:// and the next /
    pattern = r'https://(.*?)/'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError(f"Failed to extract domain from url: {url}")

def extract_page_id_from_url(url: str) -> str:
    """
    Extracts the page id from a Confluence page URL.

    :param str url: The url to a Confluence page, including the 'https://'
    :return str: The page id of the Confluence page
    """
    # Match the page id between /pages/ and the next /
    pattern = r'/pages/(\d+)/'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError(f"Failed to extract page id from url: {url}")