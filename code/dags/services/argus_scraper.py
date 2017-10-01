import logging
import os
from lxml import html
import jsonlines
import requests


class ArgusScraper(object):
    """
    Provides methods for downloading & extracting data from Argus News website
    """

    @classmethod
    def extract_headlines(cls, input_file, output_file):
        with open(input_file) as reader:
            document = html.fromstring(reader.read().strip())

            with jsonlines.open(output_file, 'w') as writer:
                for article in document.xpath('//div[@class="nq-article-card-content"]/a'):
                    writer.write({
                        'url': article.attrib['href'],
                        'headline': article.xpath('./h2/text()')[0]
                    })

    @classmethod
    def save_webpage_to_file(cls, url, file_path):
        """
        Saves the HTML from the given url and saves it to a file
        """
        # make sure the directory structure exists before attempting to save to it
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            response = requests.get(url)
            response.raise_for_status() # ensure we capture any non-successful status codes

            with open(file_path, 'w') as file_handler:
                file_handler.write(response.text)

        except requests.exceptions.RequestException as e:
            logging.error('Unable to download HTML from %s -> %s', url, e)
            raise e
