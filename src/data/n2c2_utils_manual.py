
# coding: utf-8

# In[1]:


import numpy as np
import nltk, os
from word import Word


# In[42]:


class n2c2Parser():    
    filepath =  None
    tokens = None
    tokens_dict = None
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_file(self):
        with open(self.filepath, 'r') as f:
            data = f.read()
        data = data.replace('.\n', ' \n')
        data = data.replace('-', ' ')
        data = data.replace(':', ' ')

        tokens = []
        tokens_dict = {}
        word_offset = 0
        prev_char = ' '
        current_token = ''
        start_char, end_char = None, None 
        end_of_word = {' ', '\n', r','} # tokens signifying end of word
        for i, char in enumerate(data):
            if prev_char in end_of_word and char not in end_of_word: # new word started
                start_char = i
                current_token += char
            elif prev_char not in end_of_word and char in end_of_word: # word ended
                end_char = i
                tokens.append(
                    {'text': current_token, 'start_char':  start_char, 'end_char':  end_char}
                )
                tokens_dict[start_char] = {
                    'text': current_token,
                    'start_char':  start_char,
                    'end_char':  end_char
                }
                current_token = ''
            elif prev_char not in end_of_word and char not in end_of_word: # word continues
                current_token += char
            else: # blank space followed by blank space
                pass
            prev_char = char
        self.tokens = tokens
        self.tokens_dict = tokens_dict
    
    def tag_gold_tokens(self, gold_file):
        parsed_gold = {}
        with open(gold_file, 'r') as f:
            gold_data = f.read().splitlines()
        for l in gold_data:
            data_in_line = self.parse_gold_line(l)
            for data in data_in_line:
                tagged_data = False
                for token in range(len(self.tokens)):
                    if (self.tokens[token]['start_char'] >= data['start_offset'] and
                            self.tokens[token]['end_char'] <= data['end_offset']):
                        tagged_data = True
                        self.tokens[token]['concept'] = data['concept']
                        self.tokens[token]['gold_text'] = data['text']
                        self.tokens[token]['id'] = data['id']
                if not tagged_data:
                    print('Data was not tagged for line:\n{0}'.format(data))

                                
    def parse_gold_line(self, line):
        bundle = []
        if line[0] == 'T':
            linesplit = line.split()
            _id = linesplit[0]
            concept = linesplit[1]
            if r';' not in linesplit[3]: # continuous
                start_offsets = [linesplit[2]]
                end_offsets = [linesplit[3]]
                text = linesplit[4:]
            else: # non-continuous
                offsets = ';'.join(linesplit[2:5]).split(';')
                start_offsets = [offsets[0], offsets[2]]
                end_offsets = [offsets[1], offsets[3]]
                text = linesplit[5:]

            for start_offset, end_offset in zip(start_offsets, end_offsets):
                bundle.append(
                    {
                        'id': _id,
                        'concept': concept,
                        'start_offset': int(start_offset),
                        'end_offset': int(end_offset),
                        'text': ' '.join(text),
                    }
                )
        return bundle


# # Testing

# In[43]:


input_file = 100039
data_path = '/Users/samrawal/Documents/workspace/colab/data/n2c2/track2/training_20180910/'

txt_file_path = '{0}/{1}.txt'.format(data_path, input_file)
ann_file_path = '{0}/{1}.ann'.format(data_path, input_file)


# In[44]:


parser = n2c2Parser(txt_file_path)
parser.parse_file()
tokens = parser.tokens


# In[45]:


for token in tokens:
    if token['start_char'] == 166:
        print(token)


# In[46]:


line = 'T80	Reason 17807 17824;17825 17837	paroxysmal atrial fibrillation'
line2 = 'T75	Drug 17749 17758	quinidine '
parser = n2c2Parser(txt_file_path)
parser.parse_file()
parser.tag_gold_tokens(ann_file_path)


# In[48]:


for t in parser.tokens:
    if abs(t['start_char'] - 17039) < 1:
        print(t)


# In[31]:


with open(txt_file_path, 'r') as f: data = f.read()


# In[32]:


data

