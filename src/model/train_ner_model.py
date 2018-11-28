import os, sys, pickle, glob, json
from tqdm import tqdm
PROJ_PATH = open('/tmp/PROJ_PATH.txt', 'r').read().strip()
sys.path.append(PROJ_PATH+'/src/')

from utils import preprocessing_utils as pprc
from utils.word import Word
from model.BiLSTM_CRF_Keras import BiLSTM_CRF

# input: one wordlist (squash multiple if needed)
def load_data(wordlist, word_tokenizer=None, concept_tokenizer=None,
              char_tokenizer=None):
    padded = pprc.pad_sentences(wordlist)
    sents = [[w.text for w in sent] for sent in padded]
    chars = pprc.split_words(sents, padding=True, pad_len=25)
    concepts = [[w.gold_concept for w in sent] for sent in padded]

    tokenized_words, word_tokenizer = pprc.tokenize(sents, t=word_tokenizer)
    tokenized_chars, char_tokenizer = pprc.tokenize_chars(chars)
    one_hot_concepts, concept_tokenizer = pprc.one_hot_encode(concepts,
                                                        t=concept_tokenizer)
    return ((tokenized_words, word_tokenizer),
            (tokenized_chars, char_tokenizer),
            (one_hot_concepts, concept_tokenizer))
    

train_wl_path = PROJ_PATH + '/data/n2c2/processed/100035.ser'
valid_wl_path = PROJ_PATH + '/data/n2c2/processed/100039.ser'
test_wl_path = PROJ_PATH + '/data/n2c2/processed/100187.ser'

train_data = pickle.load(open(train_wl_path, 'rb'))
valid_data = pickle.load(open(valid_wl_path, 'rb'))
test_data = pickle.load(open(test_wl_path, 'rb'))

(train_sents, word_tokenizer),  (train_chars, char_tokenizer), (train_concept, concept_tokenizer) = load_data(train_data)
(valid_sents, _),  (valid_chars, _), (valid_concept, _)  = load_data(valid_data, word_tokenizer, concept_tokenizer)
(test_sents, _),  (test_chars, _), (test_concept, _) = load_data(test_data, word_tokenizer, concept_tokenizer)


model_parameters = json.load(open(PROJ_PATH + '/src/model/config.json', 'r'))
model_parameters['vocab_size'] = len(word_tokenizer.word_index)
model_parameters['char_dim'] = len(char_tokenizer)
model_parameters['output_dim'] = len(concept_tokenizer.word_index)
model_parameters = {
    'vocab_size': len(word_tokenizer.word_index),
    'char_dim': len(char_tokenizer),
    'output_dim': len(concept_tokenizer.word_index),
}

print(model_parameters)
model = BiLSTM_CRF(model_parameters)
model.define_model()
model.generate_model_diagram()
model.train(train_sents, train_chars, train_concept, valid_sents, valid_chars, valid_concept)
