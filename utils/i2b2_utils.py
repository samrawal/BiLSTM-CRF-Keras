import numpy as np
import nltk
from word import Word

class i2b2Parser():
    filepath =  None
    data = None

    def __init__(self, filepath):
        self.filepath = filepath

    def parse_file(self):
        with open(filepath, 'r') as f:
            data = f.read().splitlines()
        tokens = []
        for linenum, line in enumerate(data):
            tokens.append(self.get_offsets(nltk.word_tokenize(line), line))

    def get_offsets(tokens, text):
        offset = 0
        offsets = []
        for token in tokens:
            offset = text.find(token, offset)
            offsets.append({'text': token, 'start': offset, 'end': offset + len(token)})
        return offsets



