import jsonlines
import logging
from textblob import TextBlob


def prove_carcinogenic_effect_with_science(headlines_file_path, use_actual_science):
    with jsonlines.open(headlines_file_path) as reader:
        for news_item in reader:
            blob = TextBlob(news_item['headline'])
            logging.info('Found %s in %s', blob.noun_phrases, news_item['headline'])

            if blob.sentiment.polarity < 0.5:
                tags = blob.tags
                proper_nouns = set(tag.lower() for tag, token in tags if token == 'NNP')

                tag_intersection = list(set.intersection(proper_nouns, blob.noun_phrases))

                if tag_intersection:
                    logging.info('## %s causes Cancer', news_item['headline'])
     