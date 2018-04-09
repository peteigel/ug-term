import requests
import re
import sys
from . import app_parser


class UGTabData:
    def __init__(self, data=None):
        self.content = None

        if data is not None:
            self.parse(data)
    
    def parse(self, data):
        try:
            self.content = data['data']['tab_view']['wiki_tab']['content']
        except KeyError:
            pass

    def print(self, bold_chords):
        open_chord_re = r'\[ch\]'
        close_chord_re = r'\[/ch\]'

        open_chord_rpl = ''
        close_chord_rpl = ''

        if bold_chords:
            open_chord_rpl = '\033[1m'
            close_chord_rpl = '\033[0m'
        
        clean_str = self.content
        clean_str = re.sub(open_chord_re, open_chord_rpl, clean_str)
        clean_str = re.sub(close_chord_re, close_chord_rpl, clean_str)

        sys.stdout.write(clean_str)
        return clean_str

def open(url: str):
    resp = requests.get(url)
    parser = app_parser.UGAppParser()
    parser.feed(resp.text)

    return UGTabData(parser.app_data)