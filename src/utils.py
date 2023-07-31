import re

def extract_domain_and_page_id(url: str) -> tuple[str, str]:
    domain = extract_domain_from_url(url)
    page_id = extract_page_id_from_url(url)
    return domain, page_id

def extract_domain_from_url(url: str) -> str:
    # Match the domain between https:// and the next /
    pattern = r'https://(.*?)/'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError(f"Failed to extract domain from url: {url}")

def extract_page_id_from_url(url: str) -> str:
    # Match the page id between /pages/ and the next /
    pattern = r'/pages/(\d+)/'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError(f"Failed to extract page id from url: {url}")