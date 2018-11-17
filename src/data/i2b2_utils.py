
# coding: utf-8

# In[1]:


import numpy as np
import nltk, os
from word import Word


# In[2]:


class i2b2Parser():    
    filepath =  None
    tokens = None
    def __init__(self, filepath):
        self.filepath = filepath
    def parse_file(self):
        with open(self.filepath, 'r') as f:
            data = f.read().splitlines()
        tokens = {}
        for linenum, line in enumerate(data):
            for tokennum, token in enumerate(line.split()):
                token = {'text': token, 'token': tokennum, 'line': linenum + 1}
                if linenum + 1 not in tokens: tokens[linenum + 1] = {}
                tokens[linenum + 1][tokennum] = token
        self.tokens = tokens
    
    def tag_gold_tokens(self, gold_file):
        parsed_gold = {}
        with open(gold_file, 'r') as f:
            gold_data = f.read().splitlines()
        for l in gold_data:
            data_in_line = self.parse_gold_line(l)
            for data in data_in_line:
                if data['start_line'] != None:
                    for line in range(data['start_line'], data['end_line']+1):
                        if data['start_line'] == data['end_line']:
                            for token in range(data['start_token'], data['end_token'] + 1):
                                self.tokens[line][token]['gold_tag'] = data['concept']
                                self.tokens[line][token]['gold_text'] = data['text']
                        else: # if multi-line annotation
                            if line == data['start_line']:
                                for token in self.tokens[line]:
                                    if token >= data['start_token']: 
                                        self.tokens[line][token]['gold_tag'] = data['concept']
                                        self.tokens[line][token]['gold_text'] = data['text']
                            elif line == data['end_line']:
                                for token in self.tokens[line]:
                                    if token <= data['end_token']: 
                                        self.tokens[line][token]['gold_tag'] = data['concept']
                                        self.tokens[line][token]['gold_text'] = data['text']
                            else:
                                for token in self.tokens[line]:
                                    self.tokens[line][token]['gold_tag'] = data['concept']
                                    self.tokens[line][token]['gold_text'] = data['text']

                                
    def parse_gold_line(self, line):
        bundle = []
        chunks = line.split('||')
        for chunk in chunks:
            split_a = chunk.split('\" ')
            concept = split_a[0].split('=')[0]
            text = split_a[0].split('=')[1][1:]
            
            split_b = split_a[1].split() if len(split_a) > 1 else []
            if len(split_b) == 0: # no start/end values here
                start_line, start_token = None, None
                end_line, end_token = None, None
                bundle.append({
                    'concept': concept,
                    'text': text,
                    'start_line': start_line,
                    'start_token': start_token,
                    'end_line': end_line,
                    'end_token': end_token,
                })

            elif r',' not in split_b[1]:
                [start_line, start_token] = split_b[0].split(':')
                [end_line, end_token] = split_b[1].split(':')
                bundle.append({
                    'concept': concept,
                    'text': text,
                    'start_line': int(start_line),
                    'start_token': int(start_token),
                    'end_line': int(end_line),
                    'end_token': int(end_token),
                })
            else:
                groups = split_a[1].split(r',')
                for group in groups:
                    [start, end] = group.split()
                    [start_line, start_token] = start.split(':')
                    [end_line, end_token] = end.split(':')
                    bundle.append({
                        'concept': concept,
                        'text': text,
                        'start_line': int(start_line),
                        'start_token': int(start_token),
                        'end_line': int(end_line),
                        'end_token': int(end_token),
                    })
        return bundle


# # Testing

# In[4]:


def parse_all_gold_train():
    count = 0
    gold_files = ['11995', '133875', '150406', '180195', '182909','18563', '189350', '210958', '241468', '379569',]
    data = {}
    for filenum in gold_files:
        colab_path = os.environ['colab']
        data_path = colab_path + '/data/i2b2/2009 Medication Challenge/'
        sample_file = data_path + '/training_sets_released_merged/{0}'.format(filenum)
        sample_file_gold = data_path + '/training_ground_truth/training.ground.truth/{0}_gold.entries'.format(filenum)
        parser = i2b2Parser(sample_file)
        parser.parse_file()
        parser.tag_gold_tokens(sample_file_gold)
        tokens = parser.tokens
        for line in tokens:
            for token in tokens[line]: count += 1
        data[filenum] = tokens
    print('{0} tokens found across {1} files.'.format(count, len(gold_files)))

