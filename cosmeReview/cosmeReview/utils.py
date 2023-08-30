import re

class URLParser:
    def __init__(self, url):
        self.url = url

    def extract_number(self, keyword):
        pattern = f'{keyword}/(\\d+)'
        match = re.search(pattern, self.url)

        if match:
            return match.group(1)
        else:
            return None

class LinkDetails:
    def __init__(self, url):
        self.url_parser = URLParser(url)
    
    def get_brand_id(self):
        return self.url_parser.extract_number('brand_id')
    
    def get_product_id(self):
        return self.url_parser.extract_number('product_id')

    def get_user_id(self):
        return self.url_parser.extract_number('user_id')

    def get_review_id(self):
        return self.url_parser.extract_number('review')