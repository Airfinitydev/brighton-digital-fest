import logging
import jsonlines
from textblob import TextBlob


exceptions = set(['injured', 'died', 'ill'])

def prove_carcinogenic_effect_with_science(headlines_file_path, use_actual_science):
    data = []

    with jsonlines.open(headlines_file_path) as reader:
        for news_item in reader:
            if not use_actual_science:
                blob = TextBlob(news_item['headline'])

                if blob.sentiment.polarity < -0.3:
                    tags = blob.tags
                    proper_nouns = set(tag.lower() for tag, token in tags if token == 'NNP')

                    tag_intersection = list(set.intersection(proper_nouns, blob.noun_phrases))

                    # in order to not be too insensitive, if the tags contain certain words, don't apply science
                    if tag_intersection and not set.intersection(set(tag.lower() for tag, token in tags), exceptions):
                        news_item['new_headline'] = '%s causes Cancer' % news_item['headline']

            data.append(news_item)

    # write back to the same file
    with jsonlines.open(headlines_file_path, 'w') as writer:
        writer.write_all(data)
