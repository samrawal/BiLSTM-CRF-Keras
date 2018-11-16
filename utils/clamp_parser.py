import xml.etree.ElementTree as ET
import pickle
from word import Word

'''
XMI FILE FORMAT:
================
all children of the root:
- child[0] => some XMI info; discard
- child[1] => raw text
- child[2] => DocumentAnnotation info
- child[3] => input file info
- child[4 : n] => sentences information
- child[n : -1] => token information
- child[-1] => ? not sure what this is
'''

def xmi2Word(xmi_filepath, filename=''):
    tree = ET.parse(xmi_filepath)
    root = tree.getroot()
    elements = [child for child in root]
    raw_text = elements[1].attrib['sofaString']
    parse = []
    sentences = []

    for e in elements[4 : ]:
        data = e.attrib
        if 'sentenceNumber' in data: # is a sentence
            sentences.append(data)
        elif 'tokenNumber' in data: # is a token
            word = Word()
            word.start_char = int(data['begin'])
            word.end_char = int(data['end'])
            word.text = raw_text[word.start_char : word.end_char]
            word.pos = data['partOfSpeech']
            word.token = int(data['tokenNumber'])
            word.filename = filename

            for s in sentences:
                if in_span(int(s['begin']), int(s['end']),
                           word.start_char, word.end_char):
                    word.sentence = int(s['sentenceNumber'])
                    break
            
            parse.append(word)
    return parse

# check if b is in span of a
def in_span(start_a, end_a, start_b, end_b ):
    return True if (start_a <= start_b and end_a >= end_b) else False
