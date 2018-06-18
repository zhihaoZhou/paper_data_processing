# -*- coding: utf-8 -*-
import nltk
import re
import os
from bio import Bio

"""
Note we have 11598 articles in total
"""


# determines if a line of symbols are meaningless
def is_meaningless(line):
    """
    :param line: string
    :return: bool
    """
    # filter out short lines
    if len(re.findall(' ', line)) < 2:
        return True
    # filter out math equations
    if len(re.findall('/', line)) + len(re.findall('\|', line)) \
            + len(re.findall('\+', line)) + len(re.findall('\\\\', line))\
            > 4:
        return True
    # filter out websites
    if len(re.findall('@', line)) + \
            len(re.findall('http', line)) != 0:
        return True
    return False


# obtain and return useful sentences from file. Sentences are tokenized
# and converted to lower case
def read_from_file(f_name):
    """
    :param f_name: str
    :return: list of list of strings
            (list of sentences where each sentence is a
            list of strings)
    """
    data = []
    f = open(f_name)
    entire_string = ''
    for line in f:
        # remove all question marks
        line = line.replace('?', '').strip().lower()
        if not is_meaningless(line):
            entire_string += line + ' '
    sentences = nltk.sent_tokenize(entire_string)
    for s in sentences:
        tokenized_s = nltk.word_tokenize(s)
        if len(tokenized_s) > 5:
            data.append(tokenized_s)
    return data


def data_to_str(data):
    """
    :param data: list of list of strings
    :return: str
    """
    data_str = ''
    for s in data:
        s = ' '.join(s)
        data_str += s + ' '
    return data_str


def calculate_offsets(document_id, words):
    """
    :param document_id: str
    :param words: list of strings
    :return: list of strings
    """
    offsets = []
    # calculate offsets
    start = 0
    for word in words:
        if word == '<eos>':
            offsets.append('<eos>')
            continue
        offsets.append(document_id + ':' + str(start) + '-' +
                       str(start + len(word) - 1))
        start += len(word) + 1
    return offsets


if __name__ == '__main__':

    i = 0
    for subdir, dirs, files in os.walk('unannotated_data/raw_articles'):
        for f in files:
            f_name = os.path.join(subdir, f)
            if not f_name.endswith(".txt"):
                continue
            data = read_from_file(f_name)

            # add to bio
            raw_text_bio = Bio()
            words = []
            for s in data:
                words.extend(s)
                words.append('<eos>')
            doc_id = re.findall('.*/.*/(.*).txt', f_name)[0]
            tags = ['O']*len(words)
            raw_text_bio.add_data(words, tags, doc_id)

            # write processed article
            processed_article = 'unannotated_data/processed_articles/' \
                                + doc_id + '.txt'
            processed_article = open(processed_article, 'w')
            data_str = data_to_str(data)
            processed_article.write(data_str)
            processed_article.close()

            # write processed article bio
            processed_bio = 'unannotated_data/processed_article_bios/' \
                            + doc_id + '.bio'
            processed_bio = open(processed_bio, 'w')
            processed_bio.write(raw_text_bio.to_str())
            processed_bio.close()
