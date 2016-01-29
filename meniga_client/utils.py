from html.parser import HTMLParser
from datetime import datetime


class TokenExtractor(HTMLParser):
    token = None

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'input' and ('name', '__RequestVerificationToken') in attrs:
            self.token = dict(attrs).get('value')


def meniga_datetime(*args):
    return "/Date({}+0000)/".format(int(datetime(*args).timestamp() * 1000))