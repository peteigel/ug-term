import re
from typing import Tuple, List, Dict
from html.parser import HTMLParser
import json

class UGAppParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.app_data = {}
        self.inline_js = ''
        self.stack = []

    # Called after all data has been recieved
    def process_results(self):
        app_data_str = None
        results = re.finditer(
            r'UGAPP\.store\.page\s*=\s*(\{.*\})\s*;', self.inline_js)
        for match in results:
            app_data_str = match[1]

        if app_data_str is None:
            return

        self.app_data = json.loads(app_data_str)

    def handle_starttag(self, tag: str, attrs):
        self.stack.append(tag)

    def handle_data(self, data: str):
        if len(self.stack) == 0:
            return

        if self.stack[-1] == 'script':
            self.inline_js = self.inline_js + '\n' + data

    def handle_endtag(self, tag):
        while self.stack[-1] != tag:
            self.stack.pop()

        self.stack.pop()

        if len(self.stack) == 0:
            self.process_results()