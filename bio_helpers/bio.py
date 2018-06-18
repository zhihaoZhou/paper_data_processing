# -*- coding: utf-8 -*-
import numpy as np
import string


# the Bio object consists a list of words, a list of their corresponding
# tags and a list of their corresponding tags
class Bio(object):
    def __init__(self):
        self.words = []
        self.tags = []
        self.offsets = []

    @staticmethod
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

    # note: add one document at a time
    def add_data(self, words, tags, document_id):
        """
        :param words: list of strings
        :param tags: list of strings
        :param document_id: str
        :return: None
        """
        offsets = self.calculate_offsets(document_id, words)
        if not (len(words) == len(tags) and len(tags) == len(offsets)):
            raise Exception('Length of arguments should match.')
        for i in range(len(words)):
            try:
                words[i] = words[i].encode('utf-8')
            except UnicodeDecodeError:
                words[i] = ''
                print "encoding error occurred but ignored"
            if all(c in string.printable for c in words[i]):
                words[i] = words[i]
            else:
                words[i] = ','

        self.words.extend(words)
        self.tags.extend(tags)
        self.offsets.extend(offsets)

    def to_str(self):
        bio_str = ''
        for i in range(len(self.words)):
            if self.words[i] == '<eos>':
                bio_str += '\n'
                continue
            line = self.words[i] + ' ' + self.offsets[i] + ' ' \
                   + self.tags[i] + "\n"
            bio_str += line
        return bio_str

    # this function converts num_sentences sentences random selected
    # from the bio object to string and returns it
    def to_str_sample(self, num_sentences):
        """
        :param num_sentences: int
        :return: str
        """
        all_sentences = []
        sentence = ''
        for i in range(len(self.words)):
            if self.words[i] == '<eos>':
                all_sentences.append(sentence)
                sentence = ''
                continue
            line = self.words[i] + ' ' + self.offsets[i] + ' ' \
                   + self.tags[i] + "\n"
            sentence += line
        all_sentences = np.array(all_sentences)
        # Randomly shuffle data
        np.random.seed(10)
        shuffle_indices = np.random.permutation(np.arange(len(all_sentences)))
        all_sentences = all_sentences[shuffle_indices]

        print len(all_sentences)
        bio_str = ''
        for i in range(num_sentences):
            bio_str += all_sentences[i] + '\n'
        return bio_str

    # this function split all data in Bio and writes them into train, dev and test files
    # given the provided percentages
    def write_tagger_inputs(self, train_percent, dev_percent, test_percent,
                            f_train, f_dev, f_test):
        """
        :param train_percent: int
        :param dev_percent: int
        :param test_percent: int
        :param f_train: str
        :param f_dev: str
        :param f_test: str
        :return: None
        """
        if not train_percent + dev_percent + test_percent == 100:
            raise Exception('Percents should add up to 100.')
        all_sentences = []
        sentence = ''
        for i in range(len(self.words)):
            if self.words[i] == '<eos>':
                all_sentences.append(sentence)
                sentence = ''
                continue
            line = self.words[i] + ' ' + self.offsets[i] + ' ' \
                   + self.tags[i] + "\n"
            sentence += line
        all_sentences = np.array(all_sentences)
        # Randomly shuffle data
        np.random.seed(10)
        shuffle_indices = np.random.permutation(np.arange(len(all_sentences)))
        all_sentences = all_sentences[shuffle_indices]

        # split data and write to the 3 files
        train_end = len(all_sentences)*train_percent/100
        f = open(f_train, 'w')
        for i in range(train_end):
            f.write(all_sentences[i] + '\n')
        f.close()
        f = open(f_dev, 'w')
        dev_start = train_end
        dev_end = dev_start + len(all_sentences)*dev_percent/100
        for i in range(dev_start, dev_end):
            f.write(all_sentences[i] + '\n')
        f.close()
        f = open(f_test, 'w')
        for i in range(dev_end, len(all_sentences)):
            f.write(all_sentences[i] + '\n')
        f.close()
