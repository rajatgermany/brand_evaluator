import tweepy

from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

import json
import pickle
import os

from app import DATA_DIRECTORY

MODEL_FILE_json = os.path.join(DATA_DIRECTORY, "model_files/model.json")
MODEL_FILE_h5 = os.path.join(DATA_DIRECTORY, "model_files/model.h5")
TOKENIZER_FILE = os.path.join(DATA_DIRECTORY, "model_files/tokenzizer.file")

from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



with open(TOKENIZER_FILE, 'rb') as file:
    tokenizer = pickle.load(file)

json_file = open(MODEL_FILE_json , 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(MODEL_FILE_h5)
print("Loaded model from disk")

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

def clean_tweet(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)
#after tweepy preprocessing the colon symbol left remain after      #removing mentions
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
#replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)
#remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)
#filter using NLTK library append it to a string
    filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []
#looping through conditions
    for w in word_tokens:
#check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    #print(word_tokens)
    #print(filtered_sentence)return tweet

def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None

def predict_sentiment(text):
    text = tokenizer.texts_to_sequences([text])
    text = pad_sequences(text, padding='post', maxlen=100)
    pred = loaded_model.predict_classes(text)
    return pred[0][0]

def get_sentiment(tokenized_tweet_text):
    sentiment = loaded_model.predict_classes(tokenized_tweet_text)
    return sentiment[0][0]


def most_frequent_words(tweets):
    all_tweets_text = ' '.join([tweet.text for tweet in tweets])
    all_tweets_text = re.sub(r"http\S+", "", all_tweets_text)
    all_tweets_text = all_tweets_text.replace('RT ', ' ').replace('&amp;', 'and')
    all_tweets_text = re.sub('[^A-Za-z0-9]+', ' ', all_tweets_text)
    all_tweets_text = all_tweets_text.lower()

    tokenized_word = word_tokenize(all_tweets_text)
    stop_words=set(stopwords.words("english"))
    filtered_sent=[]
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)
    return fdist

    
        