from typing import List

from pydantic import BaseModel


class Tweet(BaseModel):
    text: str
    sentiment: str
    created_at: str
    frequent_words: List
    user_location: str
    retweet_count: int
    favorite_count: int

class Tweets(BaseModel):
    result: List[Tweet]

class RequestSpecs(BaseModel):
    brand: str

# TODO NEED TO find the way to add the forecast type
