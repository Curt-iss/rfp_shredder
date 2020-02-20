#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

from bs4 import BeautifulSoup
from datetime import datetime
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import sys
import tarfile
from time import sleep
from typing import List

# Constants -------------------------------------------------------------------

# Setting up headless chrome -------

chrome_options = Options()
chrome_options.add_argument('--headless')

BASE_URL = 'https://beta.sam.gov/'
WEB_DRIVER = webdriver.Chrome(chrome_options=chrome_options)

# Classes ---------------------------------------------------------------------

class RFP:

    def __init__(self, rfp_url: str):
        """ When given a url, this class contains the scraped contents.
        """
        WEB_DRIVER.get(rfp_url)
        sleep(1)

        self.__soup = BeautifulSoup(WEB_DRIVER.page_source, 'html.parser')

        self.header = parse_header()

        self.gen_info = parse_gen_info()

        self.classification = parse_classification()

        self.description = parse_description()

        self.attachments = parse_attachments()

    def parse_header(self):
        """ Parse the header for this page
        """
        header = __soup.select_one('section#header')
        header_dict = dict()
        header_dict['is_active'] = header.select_one('span.sam.green.status.label.ng-star-inserted').string
        notice_id_elem, content_elem = header.select('div.content')
        header_dict['notice_id'] = notice_id_elem.select_one('div.description').string
        
        sub_headers = content_elem.select('div.header')
        sub_descriptions = content_elem.select('div.description')
        for i, child in enumerate(sub_headers):
            header_dict[child.string] = sub_descriptions[i].string

        return header_dict
    
    def parse_gen_info():
        gen_info = __soup.select_one('section#general')
        gen_info_dict = dict()

        return gen_info_dict

    def parse_classification():
        classification = __soup.select_one('section#classification')
        class_dict = dict()

        return class_dict

    def parse_description():
        description = __soup.select_one('select#description')
        description_dict = dict()

        return description_dict

    def parse_attachments():
        attachments = __soup.select_one('attachment-section')
        attachments_dict = dict()

        return attachments_dict


# Functions -------------------------------------------------------------------


def directory_size(root_dir: Path):
    # Meh, this works but I get perms errors obviously I guess
    return sum(f.stat().st_size for f in root_dir.glob('**/*') if f.is_file())


def root_path() -> Path:
    """ Platform independent of finding the root directory
    """
    # ? I think there's actually a standard library way of
    # ? doing this.
    root_str = os.path.splitdrive(sys.executable)[0]
    return Path('/') if root_str == '' else Path(root_str)


def build_search_url(
        search_terms: List[str],
        sort: str = '-relevance',
        index = 'opp',
        is_active: bool = False) -> str:
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
    return f'{BASE_URL}search?keywords={joined_terms}&sort={sort}&index={index}&is_active={str(is_active).lower()}'


def find_num_pages(search_url: str) -> int:
    """ Find the number of pages in given query
    """
    WEB_DRIVER.get(search_url)
    # Sleep to wait for the page to load
    sleep(1)
    # Turn an html response into soup
    soup = BeautifulSoup(WEB_DRIVER.page_source, 'html.parser')
    page_buttons = soup.select('a.page-button')
    # The largest page number is the next to last button
    # This normally happens to be 1000
    return int(page_buttons[-1].string)


def get_result_links(search_soup: BeautifulSoup) -> List[str]:
    """ This function scrapes the result links from a page.
    """
    # Looks like the base url is clipped off of these anchors.
    # So we'll concatenate them here
    anchors = search_soup.select('a.wordbreak.ng-star-inserted')
    return [BASE_URL + anchor['href'][1:] for anchor in anchors]

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

    num_pages = find_num_pages(search_url)

    # If I ever figure out argparse-ing, cli args could be som much better
    # wouldn't need to hardcode this stuff

    # Path to write output tarfile
    tar_path = Path(f'./sam_scrape.tar.bz2')

    # Open a tarfile writing with bz2 compression
    with tarfile.open(tar_path, 'w:bz2') as tar_file:

        # While the current dir is under 10GB
        while directory_size(Path('.')) // 2 ** 30 < 10:
            for page in range(1, num_pages + 1):

                try:
                    WEB_DRIVER.get(f'{search_url}&page={page}')
                    sleep(1)  # Sleep for a sec
                    search_page_html = WEB_DRIVER.page_source
                except Exception:
                    print(f"Couldn't fetch page #{page} ...")

                search_page_soup = BeautifulSoup(
                    search_page_html, 'html.parser')

                # Scrape the search result links off the page
                result_links = get_result_links(search_page_soup)

                for link in result_links:
                    pass

        print('VM ran out of space...\nExiting...')
