import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import numpy as np

from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import os
import json

import pickle

from app import DATA_DIRECTORY


MODEL_FILE_json = os.path.join(DATA_DIRECTORY, "model_files/model.json")
MODEL_FILE_h5 = os.path.join(DATA_DIRECTORY, "model_files/model.h5")
TOKENIZER_FILE = os.path.join(DATA_DIRECTORY, "model_files/tokenzizer.file")


maxlen = 100
embedding_dim = 50
embedding_path = os.path.join(DATA_DIRECTORY, "glove/glove.6B.100d.txt")


filepath_dict = { 'yelp':   os.path.join(DATA_DIRECTORY, 'yelp_labelled.txt'),
                 'amazon': os.path.join(DATA_DIRECTORY, 'amazon_cells_labelled.txt')
                 'imdb': os.path.join(DATA_DIRECTORY, 'imdb_labelled.txt')
                }
            
df_list = []
for source, filepath in filepath_dict.items():
    df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
    df['source'] = source  # Add another column filled with the source name
    df_list.append(df)

df = pd.concat(df_list)
df = df.reset_index(drop = True)



# Creating the token vector 
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df['sentence'].values)
X_train = tokenizer.texts_to_sequences(df['sentence'].values)

vocab_size = len(tokenizer.word_index) + 1

X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)



def create_embedding_matrix(embedding_path, word_index, embedding_dim):
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    embedding_matrix = np.zeros((vocab_size, embedding_dim))
    with open(embedding_path) as f:
        for line in f:
            word, *vector = line.split()
            if word in word_index:
                idx = word_index[word] 
                embedding_matrix[idx] = np.array(
                    vector)[:embedding_dim]

    return embedding_matrix

embedding_matrix = create_embedding_matrix( 
    embedding_path = embedding_path, 
    word_index = tokenizer.word_index ,
    embedding_dim = embedding_dim
)    

model = Sequential()
model.add(layers.Embedding(vocab_size, embedding_dim, 
                           weights=[embedding_matrix], 
                           input_length=maxlen, 
                           trainable=False))
model.add(layers.GlobalMaxPool1D())
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.summary()


y_train = list(df['label'])
history = model.fit(X_train, y_train,
                    epochs=10,
                    batch_size=30)
loss, accuracy = model.evaluate(X_train, y_train)
print("Training Accuracy: {:.4f}".format(accuracy))

model_json = model.to_json()
with open(MODEL_FILE_json, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights(MODEL_FILE_h5)
print("Saved model to disk")

with open(TOKENIZER_FILE, 'wb') as file:
    pickle.dump(tokenizer, file)