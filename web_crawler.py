import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()
found_links = set()

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawl(url, max_depth=2, depth=0):
    if depth > max_depth or url in visited:
        return

    try:
        response = requests.get(url, timeout=5)
        visited.add(url)

        if "text/html" in response.headers.get("Content-Type", ""):
            soup = BeautifulSoup(response.text, 'html.parser')

            for tag in soup.find_all(["a", "form"]):
                link = tag.get('href') or tag.get('action')
                if link:
                    full_url = urljoin(url, link)
                    if is_valid_url(full_url) and urlparse(full_url).netloc == urlparse(url).netloc:
                        found_links.add(full_url)
                        crawl(full_url, max_depth, depth + 1)

    except Exception as e:
        print(f"❌ Error crawling {url}: {str(e)}")

def get_links_for_target(target_url, depth=2):
    visited.clear()
    found_links.clear()
    crawl(target_url, max_depth=depth)
    return list(found_links)

def extract_forms_from_url(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        forms = []

        for form in soup.find_all('form'):
            form_info = {
                'action': form.get('action'),
                'method': form.get('method'),
                'inputs': []
            }
            for input_tag in form.find_all(['input', 'textarea']):
                form_info['inputs'].append({
                    'name': input_tag.get('name'),
                    'type': input_tag.get('type', 'text')
                })
            forms.append(form_info)

        return forms

    except Exception as e:
        print(f"❌ Error extracting forms from {url}: {str(e)}")
        return []