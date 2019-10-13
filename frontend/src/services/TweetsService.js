import axios from 'axios'

class TweetService {
    static getsentiment(query, successCallback, errorCallback) {
        query = "#"+query 
        const url = 'http://34.65.245.120:80/api_v1/tweet_analyzer/'
        console.log('it hits here', url)
        axios({
            method: 'post',
            url: url,
            data: {
                brand: query
            }
        }).then(successCallback).catch(errorCallback);
    }
}

export default TweetService;
