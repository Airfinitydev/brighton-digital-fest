import logging
import os
import jsonlines
import requests


def download_random_images(headlines_file_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with jsonlines.open(headlines_file_path) as reader:
        for article in reader:
            try:
                response = requests.get('https://unsplash.it/200?random', stream=True)
                response.raise_for_status() # ensure we capture any non-successful status codes

                with open(os.path.join(output_folder, '{}.jpg'.format(article['id'])), 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
            except requests.exceptions.RequestException as e:
                logging.error('Unable to download image for Article %s -> %s', article['id'], e)
