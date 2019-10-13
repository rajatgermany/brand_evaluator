# from app.core.auth_utils import get_current_user
from app.core.session import SessionData
from app.db.session import db_session
# from app.crud import tweet_db
from app.preprocessing import Preprocessing
from app.models.tweet import Tweets, RequestSpecs

from .service import TwitterTweetAnalyzer

from fastapi import APIRouter

session_data = SessionData()
preprocessing = Preprocessing()
router = APIRouter()

@router.post("/", response_model=Tweets, status_code=200)
async def TweetAnalyzer(request_specs: RequestSpecs):
    """ Route handler for the tweet analysis. Validates both request and response model

    Arguments:
        request_specs {RequestSpecs} -- Brand_Name
    
    Returns:
        [type] -- response_model(Tweets)
    """
    requested_brand = request_specs.brand
    twitter_tweet_analyzer = TwitterTweetAnalyzer(requested_brand)
    tweets = twitter_tweet_analyzer.download_tweets()
    tweets = twitter_tweet_analyzer.preprocess_tweets()
    tweets = twitter_tweet_analyzer.add_sentiment_to_tweeets()
    tweets = twitter_tweet_analyzer.add_most_frequent_words()
    tweets = twitter_tweet_analyzer.normalize_tweets()
    # try:
    #     tweet_db.save(db_session = db_session , tweets= tweets)
    # except Exception as e:
    #     return tweets
   
    return {
        'result': tweets
    }

tweet_analyzer_router = APIRouter()
tweet_analyzer_router.include_router(router, prefix="/tweet_analyzer")
