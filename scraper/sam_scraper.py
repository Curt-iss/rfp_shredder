#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

from bs4 import BeautifulSoup
from datetime import datetime
import os
from pathlib import Path
# beta.sam.gov uses Angular an make multiple server requests to build an entire
# html page, so we'll need a more robust HTTP handler
# import urllib.request
# import requests
from selenium import webdriver
import sys
import tarfile
from typing import List

# Constants -------------------------------------------------------------------

BASE_URL = 'https://beta.sam.gov/'
WEB_DRIVER = webdriver.Chrome()

# Classes ---------------------------------------------------------------------

class HTTPError(Exception):
    """ Raised when urllib.request does not return 200
    """

    def __init__(self, message, status):
        self.message = message
        self.status = status

# Functions -------------------------------------------------------------------


def root_path() -> Path:
    """ Platform independent of finding the root directory
    """
    # ? I think there's actually a standard library way of
    # ? doing this.
    root_str = os.path.splitdrive(sys.executable)[0]
    return  Path('/') if root_str == '' else Path(root_str)

def build_search_url(
        search_terms: List[str],
        sort: str = '-relevance',
        is_active: bool = True) -> str:
    """ Create a url containing the correct parameters

        Using the BASE_URL, this functions appends the given search terms
        to the url. This function also allows the search to be customized
        by changing default arguments.

        Params:
        search_terms: A list of given terms to search.
        sort: A string of the feature to sort results by, appended with '+' or '-'
            for ascending or decending, respectively
        is_active: A bool representing the status of search results

        Returns:
        str: A string of the resulting url
    """
    # There are more options available for sam.gov,
    # but it looks like they aren't necessary.
    joined_terms = '%20'.join(search_terms)
    return f'{BASE_URL}search?keywords={joined_terms}&sort={sort}&is_active={str(is_active).lower()}'

#def request(url: str) -> str:
    """ Makes a request to the url and returns a decoded response body
    """
#    with urllib.request.urlopen(search_url) as response:
#        if response.status != 200:
#            raise HTTPError(
#                f'Response status was: {response.status}',
#                response.status)
#        else:
            # sam.gov's meta specifies utf-8 encoding
#            return response.read().decode('utf-8')


def find_num_pages(search_url: str) -> int:
    """ Find the number of pages in given query
    """
    html_page = WEB_DRIVER.get(search_url).page_source
    # Turn an html response into soup
    soup = BeautifulSoup(html_page, 'html.parser')
    page_buttons = soup.find_all("a", class_='page-button')
    print(html_page)
    # The largest page number is the next to last button
    # This normally happens to be 1000
    return int(page_buttons[-2].text)

def get_result_links(search_soup: BeautifulSoup) -> List[str]:
    """ This function scrapes the result links from a page.
    """
    anchors = search_soup.find_all('a', class_='wordbreak ng-star-inserted')
    return [anchor.href for anchor in anchors]

# Main ------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Use arguments as search terms
        # Skip arg 0, always the program name
        search_terms = sys.argv[1:]
    else:
        print('Please pass search terms as cli arguments...')
        sys.exit(1)

    search_url = build_search_url(search_terms)

    try:
        num_pages = find_num_pages(search_url)
    except HTTPError as err:
        print(f'Unable to reach URL - Response Status was {err.status}')
        sys.exit(1)        
    
    # If I ever figure out argparse-ing, cli args could be som much better
    # wouldn't need to hardcode this stuff

    # Path to write output tarfile
    tar_path = Path(f'./sam_scrape.tar.bz2')

    # Open a tarfile writing with bz2 compression
    with tarfile.open(tar_path, 'w:bz2') as tar_file:

        # While my VM is under 25GB
        while root_path().stat().st_size // 2 ** 30 < 25:
            for page in range(1, num_pages + 1):

                try:
                    search_page_text = requests.get(f'{search_url}&page={page}').text
                except HTTPError as err:
                    print(f"Couldn't fetch page #{page} - Response Status was {err.status}")

                search_page_soup = BeautifulSoup(search_page_text, 'html.parser')

                # Scrape the search result links off the page
                result_links = get_result_links(search_page_soup)

                for link in result_links:
                    pass

