#!/usr/bin/env python3

# Imports ---------------------------------------------------------------------

from bs4 import BeautifulSoup
from bs4.element import NavigableString
from datetime import datetime
import json
from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import io
import sys
import tarfile
from time import sleep
from typing import List

# Constants -------------------------------------------------------------------

# Setting up headless chrome -------

chrome_options = Options()
chrome_options.add_argument('--headless')

BASE_URL = 'https://beta.sam.gov/'
WEB_DRIVER = webdriver.Chrome(options=chrome_options)

# Classes ---------------------------------------------------------------------

class RFP:

    def __init__(self, rfp_url: str):
        """ When given a url, this class contains the scraped contents.
        """
        WEB_DRIVER.get(rfp_url)
        sleep(1)
        WEB_DRIVER.execute_script('window.scrollTo(0, document.body.scrollHeight/2);')
        sleep(1)

        self.__soup = BeautifulSoup(WEB_DRIVER.page_source, 'html.parser')

        # Find Title
        title_elem = self.__soup.select_one("h1")
        self.title = title_elem.string

        self.header = self.parse_header()

        self.gen_info = self.parse_gen_info()

        self.classification = self.parse_classification()

        self.description = self.parse_description()

        self.parsed_page = {
            'header': self.header,
            'gen_info': self.gen_info,
            'classification': self.classification,
            'description': self.description
        }

        self.attachments = self.parse_attachments()

    def parse_header(self):
        """ Parse the header for this page
        """
        header = self.__soup.select_one('section#header')
        header_dict = dict()
        header_dict['is_active'] = header.select_one('span.sam.green.status.label.ng-star-inserted').string
        notice_id_elem, *_, content_elem = header.select('div.content')
        header_dict['notice_id'] = notice_id_elem.select_one('div.description').string
        
        sub_headers = content_elem.select('div.header')
        sub_descriptions = content_elem.select('div.description')
        for i, child in enumerate(sub_headers):
            header_dict[child.string] = sub_descriptions[i].string

        return header_dict
    
    def parse_gen_info(self):
        gen_info = self.__soup.select_one('section#general')
        gen_info_dict = dict()

        list_items = gen_info.select('ul.usa-unstyled-list > li')
        for item in list_items:
            if item.select_one('strong') == None:
                continue
            item_strings = [
                content.strip()
                for content in item.contents
                if type(content) is NavigableString and content != ' ']
            if len(item_strings) > 0:
                gen_info_dict[item.select_one('strong').string.strip()[:-1]] = item_strings[0]
            else:
                gen_info_dict[item.select_one('strong').string.strip()[:-1]] = item.string

        return gen_info_dict

    def parse_classification(self):
        classification = self.__soup.select_one('section#classification')
        class_dict = dict()

        list_items = classification.select('ul.usa-unstyled-list > li')
        for item in list_items:
            if item.select_one('strong') == None:
                continue
            item_strings = [
                content.strip()
                for content in item.contents
                if type(content) is NavigableString and content != ' ']
            if len(item_strings) > 0:
                class_dict[item.select_one('strong').string.strip()] = item_strings[0]
            else:
                class_dict[item.select_one('strong').string.strip()] = item.string

        return class_dict

    def parse_description(self):
        description = self.__soup.select_one('section#description')
        description_dict = dict()
        description_dict['text'] = ''

        paragraphs = description.select('p')
        for paragraph in paragraphs:
            description_dict['text'] += paragraph.string
        return description_dict

    def parse_attachments(self):
        attachments = self.__soup.select_one('attachment-section')
        attachment_links = {a.contents[0]: a['href'] for a in attachments.select('a.file-link.ng-star-inserted')}

        return attachment_links


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
    anchors = search_soup.select('a.wordbreak')
    return [BASE_URL + anchor['href'][1:] for anchor in anchors]

# Main ------------------------------------------------------------------------


if __name__ == '__main__':
    #if len(sys.argv) > 1:
        # Use arguments as search terms
        # Skip arg 0, always the program name
    #    search_terms = sys.argv[1:]
    #else:
    #    print('Please pass search terms as cli arguments...')
    #    sys.exit(1)

    search_url = build_search_url([])

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

                for i, link in enumerate(result_links):
                    print(f'Processing results: {i}')

                    # Parse the current page
                    # If anything goes wrong, just skip to the next result
                    try:
                        current_rfp = RFP(link)
                    except Exception as _:
                        continue

                    
                    # turn the body into a json string
                    body_io = io.BytesIO(str.encode(json.dumps(current_rfp.parsed_page)))
                    # Create an info object describing the file
                    body_info = tarfile.TarInfo(name=f'{current_rfp.title}_body.json')

                    # Seek to the end of string and get length
                    body_info.size = body_io.seek(0, 2)
                    # Seek beginning of string
                    body_io.seek(0, 0)

                    tar_file.addfile(tarinfo=body_info, fileobj=body_io)

                    for file_name, file_link in current_rfp.attachments.items():
                        file_name = file_name.strip().replace(' ', '_')
                        file_name = file_name.replace('(', '')
                        file_name = file_name.replace(')', '')
                        file_name = Path(file_name)
                        file_name.touch()
                        # wget file
                        try:
                            subprocess.run(f'wget -O {file_name} {file_link}', shell=True)
                            sleep(1)
                        except Exception:
                            # This will normally fail when the filename is invalid on *nix
                            file_name.unlink()
                            continue

                        # write file to tar
                        tar_file.add(file_name)
                        # Delete file
                        file_name.unlink()




        print('VM ran out of space...\nExiting...')
