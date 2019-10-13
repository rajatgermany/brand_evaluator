import nltk
try:
    nltk.data.find(nltk.corpus)
except Exception:
    nltk.download('popular')