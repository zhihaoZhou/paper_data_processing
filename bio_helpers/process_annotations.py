# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import nltk
import os
import re
from bio import Bio

"""
This script converts all annotated data in annotations dir to bio format
"""


def tag_title(title_words, term_type_dict):
    """
    :param title_words: list of strings
    :param term_type_dict: dict
    :return: list of strings
    """
    title_tags = ['O']*len(title_words)
    terms = term_type_dict.keys()
    terms.sort(key=len)
    terms.reverse()
    for term in terms:
        type = term_type_dict[term]
        term_arr = term.split(' ')
        # try to find this term in the title
        # if found, tag the term in the title
        for i in range(len(title_words) - len(term_arr) + 1):
            is_found = True
            for j in range(len(term_arr)):
                # note we only tag titles which haven't been tagged
                if title_words[i + j] != term_arr[j] or title_tags[i + j] != 'O':
                    is_found = False
                    break
            if is_found:
                title_tags[i] = 'B-' + type
                for j in range(1, len(term_arr)):
                    title_tags[i + j] = 'I-' + type
    return title_tags


def read_file(f_name, abstracts, titles):
    """
    :param f_name: str
    :param abstracts: Bio
    :param titles: Bio
    :return: None
    """
    tree = ET.parse(f_name)
    root = tree.getroot()
    title = root[0]
    title_words = nltk.word_tokenize(title.text.lower())
    title_words.append('<eos>')
    content = root[1]

    abstract_words = []
    abstract_tags = []
    term_type_dict = dict()
    for s in content.findall('S'):
        if s.text:
            text_arr = nltk.word_tokenize(s.text.lower())
            abstract_words.extend(text_arr)
            abstract_tags.extend(['O']*len(text_arr))
        for term in s.findall('term'):
            type = term.get('class').upper()
            if type == 'LR-PROD':
                type = 'LRPROD'
            if term.text:
                term_arr = nltk.word_tokenize(term.text.lower())
                abstract_words.extend(term_arr)
                abstract_tags.append('B-'+type)
                abstract_tags.extend(['I-'+type]*(len(term_arr) - 1))
                # add this term to terms
                term_str = ' '.join(term_arr)
                term_type_dict[term_str] = type

            if term.tail:
                text_arr = nltk.word_tokenize(term.tail.lower())
                abstract_words.extend(text_arr)
                abstract_tags.extend(['O'] * len(text_arr))
        abstract_words.append('<eos>')
        abstract_tags.append('<eos>')

    # tag title
    title_tags = tag_title(title_words, term_type_dict)

    # calculate document_id
    document_id = re.findall('.*/.*/.*/(.*).xml', f_name)[0]

    # add data to Bio object
    abstracts.add_data(abstract_words, abstract_tags, document_id)
    titles.add_data(title_words, title_tags, document_id)


if __name__ == '__main__':
    abstracts = Bio()
    titles = Bio()
    total_document_num = 0
    for subdir, dirs, files in os.walk('annotations'):
        for file in files:
            f_name = os.path.join(subdir, file)
            if not f_name.endswith(".xml"):
                continue
            total_document_num += 1
            read_file(f_name, abstracts, titles)

    abstract_train_f = 'annotations_bio/abstract_train.bio'
    abstract_dev_f = 'annotations_bio/abstract_dev.bio'
    abstract_test_f = 'annotations_bio/abstract_test.bio'
    abstracts.write_tagger_inputs(70, 20, 10, abstract_train_f, abstract_dev_f, abstract_test_f)

    print titles.to_str()
    print total_document_num


