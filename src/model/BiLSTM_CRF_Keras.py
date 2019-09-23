import os, sys, pickle, glob
from tqdm import tqdm
PROJ_PATH = open('/tmp/PROJ_PATH.txt', 'r').read().strip()
sys.path.append(PROJ_PATH+'/src/')

import numpy as np
#import keras
from keras.models import Model, load_model
from keras.layers import Input, Embedding, LSTM, Dense, TimeDistributed, Reshape, Bidirectional, concatenate, Flatten
from keras_contrib.layers import CRF
from keras.utils import plot_model

class BiLSTM_CRF():
    embedding_dim = None
    num_epochs = None
    max_sentence = None
    max_word = None
    model_title = None
    vocab_size = None
    output_dim = None
    char_dim = None

    model = None
    
    def __init__(self, params=None, title=None):
        self.set_params(params, title)

    def set_params(self, params, title):
        self.model_title = title if title != None else 'untitled_BiLSTM-CRF'      
        self.embedding_dim = 100
        self.num_epochs = 10
        self.max_sentence = 20
        self.max_word = 25
        self.vocab_size = 500
        self.char_dim = 99
            
        if params != None:
            if 'embedding_dim' in params and params['embedding_dim'] != None:
                self.embedding_dim = params['embedding_dim']
            if 'num_epochs' in params and params['num_epochs'] != None:
                self.num_epochs = params['num_epochs']
            if 'max_sentence' in params and params['max_sentence'] != None:
                self.max_sentence = params['max_sentence']
            if 'max_word' in params and params['max_word'] != None:
                self.max_word  = params['max_word']
            if 'vocab_size' in params and params['vocab_size'] != None:
                self.vocab_size = params['vocab_size']
            if 'output_dim' in params and params['output_dim'] != None:
                self.output_dim = params['output_dim']
            if 'char_dim' in params and params['char_dim'] != None:
                self.char_dim = params['char_dim']

    def define_model(self, char_embedding_dim = 120, word_embedding_dim=120, char_lstm_cell=20, lstm_cell=20):
        # distributional word representation: embeddings (TODO: GloVe/word2vec)
        word_input = Input(shape=(self.max_sentence,), name="word_input")
        #embedding_weights = we.get_word2vec_embeddings(embedding_model, word_tokenizer, embedding_dim)
        word = Embedding(input_dim=self.vocab_size+1, output_dim=word_embedding_dim,
                        #weights=[embedding_weights],
                        input_length=self.max_sentence,
                        trainable=False
        )(word_input)

        # orthographic word representation: char embeddings -> BiLSTM
        char_input = Input(shape=(self.max_sentence, self.max_word), name="char_input")
        char = TimeDistributed(
            Embedding(input_dim=self.char_dim, output_dim = char_embedding_dim,
                        input_length=self.max_word)
        )(char_input)
        char = TimeDistributed(
            Bidirectional(
                LSTM(char_lstm_cell, return_sequences=True),
                merge_mode='concat'
            )
        )(char)
        char = TimeDistributed(Flatten())(char)

        # concatenate word + char representations
        inputs = concatenate([word, char])

        # main BiLSTM model
        model = Bidirectional(
            LSTM(lstm_cell, return_sequences=True),
            merge_mode='concat'
        )(inputs)
        model = TimeDistributed(
            Dense(self.output_dim, activation='softmax')
        )(model)
        crf = CRF(self.output_dim, name="output")
        output = crf(model)

        m = Model(inputs=[word_input, char_input], outputs=output)
        m.compile(
            loss=crf.loss_function,
            optimizer='adam',
            metrics=[crf.accuracy]
        )

        self.model = m

    def generate_model_diagram(self, save_dir, model_name=self.model_title):
        self.model.summary()
        plot_model(self.model,
                to_file=save_dir + '{0}_architecture.png'.format(model_name),
                show_shapes=True)

    def train(self, train_sents, train_chars, train_ner,
                valid_sents=None, valid_chars=None, valid_ner=None):

        self.model.fit({"word_input": train_sents, "char_input": train_chars}, {"output": train_ner},
            #validation_data=([valid_sents, valid_chars], [valid_ner]),
            epochs=self.num_epochs,
        )

    def eval(self, model, test_sents, test_chars, test_ner):
        evaluation = model.evaluate(x=[test_sents, test_chars], y=test_ner)
        return '{0}: {1}'.format(model.metrics_names, evaluation)

    # via https://github.com/keras-team/keras-contrib/issues/129#issuecomment-399125152
    # helper function to load model
    def create_custom_objects(self):
        instanceHolder = {"instance": None}
        class ClassWrapper(CRF):
            def __init__(self, *args, **kwargs):
                instanceHolder["instance"] = self
                super(ClassWrapper, self).__init__(*args, **kwargs)
        def loss(*args):
            method = getattr(instanceHolder["instance"], "loss_function")
            return method(*args)
        def accuracy(*args):
            method = getattr(instanceHolder["instance"], "accuracy")
            return method(*args)
        return {"ClassWrapper": ClassWrapper ,"CRF": ClassWrapper, "loss": loss, "accuracy":accuracy}

    def save_model(self, save_dir, model_name=self.model_title):
        self.model.save('{0}/{1}.h5'.format(save_dir, model_name))

    def load_model(self, path):
        model = load_model(path, custom_objects=self.create_custom_objects())
        return model

    
