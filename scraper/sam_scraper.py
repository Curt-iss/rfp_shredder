#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import urllib.request
import sys
import tarfile
from typing import List

# Constants -------------------------------------------------------------------

BASE_URL = 'https://beta.sam.gov/'

# Classes ---------------------------------------------------------------------

# Functions -------------------------------------------------------------------


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

def find_num_pages(search_url: str) -> int:
    """ Find the number of pages in given query
    """
    with urllib.request.urlopen(search_url) as response:
        # sam.gov's meta specifies utf-8 encoding
        html_page = response.read().decode('utf-8')
        # Parse an html page
        soup = BeautifulSoup(html_page, 'html.parser')

    return 0


# Main ------------------------------------------------------------------------


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Use arguments as search terms
        # Skip arg 0, always the program name
        search_terms = sys.argv[1:]
    else:
        print('Please pass search terms as cli arguments...')

    search_url = build_search_url(search_terms)

    num_pages = find_num_pages(search_url)

    # If I ever figure out argparse-ing, cli args could be som much better
    # wouldn't need to hardcode this stuff

    # Path to write output tarfile
    tar_path = Path(f'./sam_scrape_{datetime.now().isoformat()}.tar.bz2')

    # Open a tarfile writing with bz2 compression
    with tarfile.open(tar_path, 'w:bz2') as tar_file:
        
        
        # While the tarfile is under 20GB
        while tar_path.stat().st_size // 2 ** 30 < 20:
            pass

