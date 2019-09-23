import os, sys, pickle, glob, json
from random import shuffle
from tqdm import tqdm
PROJ_PATH = open('/tmp/PROJ_PATH.txt', 'r').read().strip()
sys.path.append(PROJ_PATH+'/src/')

from utils import preprocessing_utils as pprc
from utils.word import Word
from utils.tracker import Tracker
from model.BiLSTM_CRF_Keras import BiLSTM_CRF

# input: one wordlist (squash multiple if needed)
def load_data(wordlist, word_tokenizer=None, concept_tokenizer=None,
              char_tokenizer=None):
    padded = pprc.pad_sentences(wordlist)
    sents = [[w.text for w in sent] for sent in padded]
    chars = pprc.split_words(sents, padding=True, pad_len=25)
    concepts = [[w.get_concept_tag() for w in sent] for sent in padded]

    tokenized_words, word_tokenizer = pprc.tokenize(sents, t=word_tokenizer)
    tokenized_chars, char_tokenizer = pprc.tokenize_chars(chars)
    one_hot_concepts, concept_tokenizer = pprc.one_hot_encode(concepts,
                                                        t=concept_tokenizer)
    return ((tokenized_words, word_tokenizer),
            (tokenized_chars, char_tokenizer),
            (one_hot_concepts, concept_tokenizer))
    

def combine_wordlists(wordlists_path):
    wl_paths = glob.glob(wordlists_path + '/*.ser')
    master_wordlist = []
    for wl in tqdm(wl_paths, 'Combining wordlists'):
        master_wordlist.extend(pickle.load(open(wl, 'rb')))
    return master_wordlist
    

def train_ner_model(wordlists_path):
    master = combine_wordlists(PROJ_PATH + '/' + wordlists_path)
    train_valid_split = int(len(master) * 0.8)
    train_data = master[0 : train_valid_split]
    valid_data = master[train_valid_split : ]


    (train_sents, word_tokenizer),  (train_chars, char_tokenizer), (train_concept, concept_tokenizer) = load_data(train_data)
    (valid_sents, _),  (valid_chars, _), (valid_concept, _)  = load_data(valid_data, word_tokenizer, concept_tokenizer)
    #(test_sents, _),  (test_chars, _), (test_concept, _) = load_data(test_data, word_tokenizer, concept_tokenizer)


    config = json.load(open(PROJ_PATH + '/src/model/config.json', 'r'))

    model_parameters = config['parameters']
    model_parameters['vocab_size'] = len(word_tokenizer.word_index)
    model_parameters['char_dim'] = len(char_tokenizer)
    model_parameters['output_dim'] = len(concept_tokenizer.word_index)

    model_info = config['model_info']
    tracker = Tracker(basedir=PROJ_PATH + '/models/',
                      desc=model_info['model_description'],
                      title=model_info['model_title'],
                      enter_desc=False,
                      name=model_info['username'],
    )

    model = BiLSTM_CRF(model_parameters)

    model.define_model(
        char_embedding_dim = model_parameters['char_embedding_dim'],
        word_embedding_dim = model_parameters['word_embedding_dim'],
        char_lstm_cell = model_parameters['char_lstm_cell'],
        lstm_cell = model_parameters['lstm_cell'],
    )

    model.generate_model_diagram(tracker.get_model_dir(), tracker.title)
    model.train(train_sents, train_chars, train_concept, valid_sents, valid_chars, valid_concept)
    model.save_model(tracker.get_model_dir(), tracker.title)

    # save tokenizers
    pickle.dump(word_tokenizer,
                open(tracker.get_model_dir() + '/word_tokenizer.ser', 'wb'))
    pickle.dump(char_tokenizer,
                open(tracker.get_model_dir() + '/char_tokenizer.ser', 'wb'))
    pickle.dump(concept_tokenizer,
                open(tracker.get_model_dir() + '/concept_tokenizer.ser', 'wb'))

    tracker.log()
