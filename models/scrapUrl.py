import requests
from bs4 import BeautifulSoup

class ScrapUrl:

    def scrapUrl(url):

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # find all the text on the page
        text = soup.get_text()
        # find the content div
        content_div = soup.find('div', {'class': 'mw-parser-output'})
        # remove unwanted elements from div
        unwanted_tags = ['sup', 'span', 'table', 'ul', 'ol']
        for tag in unwanted_tags:
            for match in content_div.findAll(tag):
                match.extract()

        #print(content_div.get_text())

        return content_div.get_text()