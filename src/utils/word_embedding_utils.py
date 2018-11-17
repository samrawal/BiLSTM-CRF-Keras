import numpy as np
from gensim.models import Word2Vec

def get_word2vec_embeddings(modelpath, tokenizer, embedding_dim):
    vocab_size = len(tokenizer.word_index)
    embedding_matrix = np.zeros((vocab_size+1, embedding_dim))
    model = Word2Vec.load(modelpath)
    for word, i in tokenizer.word_index.items():
        if word in model:
            embedding_matrix[i] = model.wv[word]
    return embedding_matrix
