# Sam Rawal <samrawal@asu.edu>

# contains functions to load data in the CoNLL 2003 format
# see https://github.com/Franck-Dernoncourt/NeuroNER/tree/master/data/conll2003/en
# https://opendata.stackexchange.com/questions/7250/corpus-of-tagged-text-english-newspapers-or-any-tagged-text/7280#7280
# for more information

import numpy as np

# parse and process data in the CoNLL 2003 format
# format of data: word, POS_tag, chunk_tag, NER_tag
class CoNLLParser():
    class Word():
        word = None
        pos = None
        chunk = None
        ner = None

        def __init__(self, word, pos, chunk, ner):
            self.word = word
            self.pos = pos
            self.chunk = chunk
            self.ner = ner

    filepath = None
    data = []
    max_sentence = 0

    def __init__(self, filepath):
        self.filepath = filepath
        self.parse_datafile()

    # store datafile into a list of lists (words -> sentence -> sentences)
    # called automatically on init
    def parse_datafile(self):
        with open(self.filepath, 'r') as df:
            lines = df.readlines()
        parsed_lines = [self.split_line(l.strip()) for l in lines]
        if parsed_lines[0].word == '-DOCSTART-' and parsed_lines[1] is None:
            parsed_lines = parsed_lines[2:]
        sentence = []
        for x in range(len(parsed_lines)):
            if parsed_lines[x] is None:
                self.data.append(sentence)
                self.max_sentence = max(self.max_sentence, len(sentence))
                sentence = []
            else:
                sentence.append(parsed_lines[x])

    # helper function for parse_datafile()
    def split_line(self, line):
        if len(line) == 0:
            return None
        else:
            s = line.split(' ')
            return self.Word(s[0], s[1], s[2], s[3])

    # pad data to pad_len. If data is longer, truncate it to fit 
    def pad_data(self, pad_len):
        unpadded_data = self.data
        padded_data = []
        for s in self.data:
            if pad_len > len(s):
                p_s = [self.Word('PADDING_TOKEN', 'X', 'X', 'X')] * pad_len
                p_s[pad_len - len(s):] = s
                padded_data.append(p_s)
            else:
                padded_data.append(s[:pad_len])
        self.data = padded_data
    # return only words in format: [[w, w, w...], [w, w, w...], ...]
    def get_sentences(self):
        return np.array([[w.word for w in s] for s in self.data])
    # return only NER tags in format: [[t, t, t...], [t, t, t...], ...]
    def get_ner(self):
        return np.array([[w.ner for w in s] for s in self.data])
