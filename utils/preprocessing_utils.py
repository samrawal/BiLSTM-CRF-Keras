# Sam Rawal <samrawal@asu.edu>

import numpy as np
from keras.preprocessing.text import Tokenizer

# TOOLS FOR KERAS TOKENIZER
# ==========================

# Take sentences in format: [[w, w, w...], [w, w, w...], ...] and return
# sequence in same structure, but with the words tokenized (as ints)
# Can fit new tokenizer (training data) or use existing tokenizer (testing)
def tokenize(sentences, t=None):
    if not t:
        tokenizer = Tokenizer(lower=False)
        tokenizer.fit_on_texts(sentences.tolist() +
                               [['PADDING_TOKEN', 'UNKNOWN_TOKEN']])
    else:
        tokenizer = t
    return np.array([[tokenizer.word_index[w] if w in tokenizer.word_index else tokenizer.word_index['UNKNOWN_TOKEN'] for w in s] for s in sentences]), tokenizer

# Tokenize and pad a single sentence. Useful when sampling trained model
# Sentence input: string
# Sentence output: [[t, t, t...]]
def tokenize_pad(sentence, tokenizer, padding):
    padded = ['PADDING_TOKEN'] * padding
    s = sentence.strip().split(' ')
    if len(s) > padding:
        padded = s[:padding]
    else:
        padded[padding-len(s):] = s
    return tokenize_sentences(np.array([padded]), t=tokenizer)

# Convert tokens back to original representations from tokenizer
# Input format: [[t, t, t...], [t,t,t...]...]
def detokenize(sentence, tokenizer):
    reverse_tokens = {v: k for k, v in tokenizer.word_index.items()}
    return [[reverse_tokens[w[0]] for w in s] for s in sentence]
    

# TOOLS FOR ONE-HOT 
# =================

# Given list of words/tags (strings), one-hot encode them with a
# new tokenizer (training data) or existing tokenizer (testing)
def one_hot_encode(tags, t=None):
    if not t:
        tokenizer = Tokenizer(lower=False)
        tokenizer.fit_on_texts(tags.tolist())
    else:
        tokenizer = t
    return np.array([[one_hot_help(w, tokenizer) for w in s] for s in tags]), tokenizer

# decode one-hot encoded sentences in format
# [[[0,1,0], [1,0,0]...], [[0,1,0], [0,0,1],...],...]
# into integer representations
def one_hot_decode(tags):
    return np.array([[np.argmax(w) + 1 for w in s] for s in tags])

# helper function for one_hot_encode()
def one_hot_help(tag, tokenizer):
    one_hot_tag = np.zeros(len(tokenizer.word_index))
    one_hot_tag[tokenizer.word_index[tag] - 1] = 1
    return one_hot_tag
    

# TOOLS FOR DICT-BASED
# ====================

# tokenize 3D data with a dictionary. Use to tokenize chars
# return tokenized values + dict to map them back
# NOTE: input needs to have chars split already if padding
def dict_tokenize(mapper, sents):
    x = np.array([[np.array([mapper[c] for c in word]) for word in sent] for sent in sents])
    return x, mapper

def dict_detokenize(tokenizer, sents):
    reverse_tokens = {v: k for k, v in tokenizer}
    x = [[[reverse_tokens[char] for char in word] for word in sent] for sent in sents]
    return x

# helper to specifically tokenize characters
def tokenize_chars(sents):
    chars = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,-_()[]{}!?:;#'\"/\\%$`&=*+@^~|"    
    mapper = {'PADDING_TOKEN': 0, 'UNKNOWN_TOKEN': 1}
    for c in chars:
        mapper[c] = len(mapper)
    return dict_tokenize(mapper, sents)
    

# helper function. When splitting sentences -> words -> chars, sentences will
# already be padded via CoNLLParser object in <conll_utils.py>. This also pads
# characters in the same way.
# Input format: [[w, w, w,...], [w, w, w,...],...]
# Output forma: [[[c,c,c,...],[c,c,c...],...],...] (padded)
def split_words(sents, padding=False, pad_len=None):
    # split individual words into lists of chars (3D->4D: (sent, words, chars))
    split_sents = [[[char for char in word] for word in sent] for sent in sents]
    if not padding:
        return split_sents
    else:
        if not pad_len: # if None, pad to longest word
            pad_len = 0
            for sent in sents: pad_len = max(pad_len, max(len(word) for word in sent))
        padded_data = []
        for s in split_sents:
            padded_sentence = []
            for w in s:
                if pad_len > len(w):
                    p_w = ['PADDING_TOKEN'] * pad_len
                    p_w[pad_len - len(w):] = w
                else:
                    p_w = w[:pad_len]
                padded_sentence.append(p_w)
            padded_data.append(padded_sentence)
        return np.array(padded_data)
