import requests
import re
from urllib.parse import quote
from typing import Tuple, List, Dict
from html.parser import HTMLParser
import json

from . import config
from . import app_parser


class UGSearchResult:
    def __init__(self, data: dict = None):
        self.url: str = None
        self.title: str = None
        self.version: int = None
        self.artist: str = None
        self.type: str = None
        self.rating: float = None

        if data is not None:
            self.parse(data)

    def parse(self, data: dict):
        if 'song_name' in data:
            self.title = data['song_name']

        if 'artist_name' in data:
            self.artist = data['artist_name']

        if 'tab_url' in data:
            self.url = data['tab_url']

        if 'type_name' in data:
            self.type = data['type_name']

        if 'rating' in data:
            self.rating = data['rating']

        if 'version' in data:
            self.version = data['version']

    def print(self):
        desc_strs = []

        if self.version is not None:
            desc_strs.append(f'Version {self.version}')
        
        if self.rating is not None:
            desc_strs.append('*' * round(self.rating))
        
        print(f'\n{self.title} - {self.artist} ({self.type})')
        
        if len(desc_strs) > 0:
            print('  ' + ' - '.join(desc_strs))
        
        print(f'  {self.url}')


def search(keyword: str) -> List[UGSearchResult]:
    search_url = f'''{
            config.UG_BASE_URL
        }/search.php?search_type=title&value={
            quote(keyword)
        }'''

    resp = requests.get(search_url)
    parser = app_parser.UGAppParser()
    parser.feed(resp.text)

    try:
        raw_results = parser.app_data['data']['results']
        return [ UGSearchResult(r) for r in raw_results]
    except KeyError:
        return None
