import requests
from bs4 import BeautifulSoup
from sitemap_generator import Sitemap

sitemap_generator = Sitemap()

BASE_URL = 'https://lists.dropfilter.app/lists'

def get_all_supported_service_indexes():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        if link.get('href') is not None:
            urls.append(link.get('href'))

    urls.pop(0)
    return urls

def get_all_drop_lists_from_service_index(service_index_url):
    response = requests.get(f"{BASE_URL}/{service_index_url}")
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        if link.get('href') is not None:
            urls.append(link.get('href'))

    urls.pop(0)
    return urls

def main():
    sitemap_generator.index_required = True
    sitemap_generator.sitemap_url = 'https://lists.dropfilter.app/'

    service_index_urls = get_all_supported_service_indexes()
    for service_index_url in service_index_urls:
        sitemap_generator.add(f"{BASE_URL}/{service_index_url}", changefreq='daily', priority=0.9)
        drop_list_urls = get_all_drop_lists_from_service_index(service_index_url)
        for drop_list_url in drop_list_urls:
            sitemap_generator.add(f"{BASE_URL}/{service_index_url}{drop_list_url}", changefreq='monthly', priority=1.0)
    sitemap_generator.write()

if __name__ == '__main__':
    main()

