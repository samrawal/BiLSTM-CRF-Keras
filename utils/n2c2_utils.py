
# coding: utf-8

# In[1]:


import clamp_parser as clamp


# In[3]:


class n2c2Parser():    
    filepath =  None
    tokens = None
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_file(self, clamp_filepath):
        self.tokens = clamp.xmi2Word(clamp_filepath)
        
    def tag_gold_tokens(self, gold_file):
        parsed_gold = {}
        with open(gold_file, 'r') as f:
            gold_data = f.read().splitlines()
        for l in gold_data:
            data_in_line = self.parse_gold_line(l)
            for data in data_in_line:
                tagged_data = False
                for token in range(len(self.tokens)):
                    if (self.tokens[token].start_char >= data['start_offset'] and
                            self.tokens[token].end_char <= data['end_offset']):
                        tagged_data = True
                        self.tokens[token].gold_concept = data['concept']
                        self.tokens[token].gold_text = data['text']
                        self.tokens[token].gold_id = data['id']
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


# In[2]:


def test():
    txt_file = '/Volumes/GoogleDrive/My Drive/Colab Notebooks/data/n2c2/track2/training_20180910/100035.txt'
    ann_file = '/Volumes/GoogleDrive/My Drive/Colab Notebooks/data/n2c2/track2/training_20180910/100035.ann'
    clamp_file = '/Volumes/GoogleDrive/My Drive/Colab Notebooks/data/n2c2/clamp-parsed/track2-training/output/100035.xmi'

    parser = n2c2Parser(txt_file)
    parser.parse_file(clamp_file)
    parser.tag_gold_tokens(ann_file)

