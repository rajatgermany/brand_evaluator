
import tweepy

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

import re
import json
import pickle
import os

from app import DATA_DIRECTORY

TOKENIZER_FILE = os.path.join(DATA_DIRECTORY, "model_files/tokenzizer.file")

with open(TOKENIZER_FILE, 'rb') as file:
    tokenizer = pickle.load(file)

emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

emoticons = emoticons_happy.union(emoticons_sad)

class Preprocessing:
    def __init__(self, type = 'hello'):
       self.type = "hello"

    def clean_tweet_text(self, tweet_text):
        if "RT @" in tweet_text:
            tweet_text = tweet_text.split("RT @")[1]
        if "https" in tweet_text:
            tweet_text = tweet_text.split('https')[0]

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(tweet_text)
    #after tweepy preprocessing the colon symbol left remain after      #removing mentions
        tweet_text = re.sub(r':', '', tweet_text)
        self.tweet_text = re.sub(r'‚Ä¶', '', tweet_text)
    #replace consecutive non-ASCII characters with a space
        tweet_text = re.sub(r'[^\x00-\x7F]+',' ', tweet_text)
    #remove emojis from tweet
        tweet_text = emoji_pattern.sub(r'', tweet_text)
    #filter using NLTK library append it to a string
        filtered_text = [w for w in word_tokens if not w in stop_words]
        filtered_text = []
    #looping through conditions
        for w in word_tokens:
    #check tokens against stop words , emoticons and punctuations
            if w not in stop_words and w not in emoticons:
                filtered_text.append(w)
        return ' '.join(filtered_text)

    def tokenize_tweet_text(self, tweet_text):
        tweet_text = tokenizer.texts_to_sequences([tweet_text])
        tweet_text = pad_sequences(tweet_text, padding='post', maxlen=100)
        return tweet_text
        


