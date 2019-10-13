import React, {Component} from 'react';
import Plot from 'react-plotly.js';

const getSentiments = (tweets) => { 
    console.log("tweets", tweets)
    return tweets.map(( tweet) => {
        return tweet.item.sentiment

    })
}

const getRange = (tweets) => {
    return tweets.map(( tweet) => {
        return tweet.item.created_at

    })
}

const getFrequentWordsXaxis = (tweets) => {
    return tweets[0].item.frequent_words.map( (frequent_word) => {
        return frequent_word[0]

    })
}

const getFrequentWordsYaxis = (tweets) => {
    return tweets[0].item.frequent_words.map( (frequent_word) => {
        return frequent_word[1]

    })
}

const getRetweetCount = (tweets) => {
    return tweets.map((tweet) => {
        return tweet.item.retweet_count

    })
}

const getFavouriteCount = (tweets) => {
    return tweets.map((tweet) => {
        return tweet.item.favorite_count

    })
}
class Graph extends Component {
    constructor(props) {
        super(props)
        this.handleOnHover = this.handleOnHover.bind(this)
      }
      
      handleOnHover(e) {
          const tweet_id = Math.floor(e.xvals)
          const tweet = this.props.tweets[tweet_id]
        //   this.hoverInfo.innerHTML = tweet.item.text
      }

      handleUnhover() {
        var infotext = 'hello'
        if ( this.hoverInfo) {
            this.hoverInfo.innerHTML = ""
        }
    }
  
      render() {
        if (this.props.tweets === "") {
            return null
        }
          const sentiments = getSentiments(this.props.tweets)
          const range = getRange(this.props.tweets)
          
        return (
            <div>
                <div id='hoverInfo' ref={ (el) => this.hoverInfo = el }></div>
                <Plot
                    data={[
                    { 
                        x : range,
                        y: sentiments,
                        type: 'scatter',
                        mode: 'lines+markers',
                        marker: {color: 'green'},
                    }
                    ]}
                    onHover = {(this.handleOnHover)}
                    onUnhover = {this.handleUnhover}
                    layout={{width: 600, height: 500, title: 'Intent Evaluation'}}
                />
                <Plot
                    data={[
                    { 
                        x: getFrequentWordsXaxis(this.props.tweets),
                        y: getFrequentWordsYaxis(this.props.tweets),
                        type: 'bar',
                        marker: {
                            color: 'rgb(142,124,195)'
                     }}
                    ]}
                    
                    layout= {{
                        title: 'Frequent Topics in Tweets',
                        width: 600, 
                        height: 500,
                        font:{
                            family: 'Raleway, sans-serif'
                        },
                        xaxis: {
                            tickangle: -45
                        },
                }}
                    
                />

                <Plot
                    data={[
                    { 
                        y: getRetweetCount(this.props.tweets),
                        type: 'bar',
                        marker: {
                            color: 'red'
                    }}
                    ]}
                    
                    layout= {{
                        title: 'Number of times tweets of brand handle Retweeted',
                        width: 600, 
                        height: 500,
                        font:{
                            family: 'Raleway, sans-serif'
                        },
                        xaxis: {
                            tickangle: -45
                        },
                    }}
                
                />

                <Plot
                    data={[
                    { 
                        y: getFavouriteCount(this.props.tweets),
                        type: 'bar',
                        marker: {
                            color: 'blue'
                    }}
                    ]}
                    layout= {{
                        title: 'Number of times tweets of brand handle Liked',
                        width: 600, 
                        height: 500,
                        font:{
                            family: 'Raleway, sans-serif'
                        },
                        xaxis: {
                            tickangle: -45
                        },
                    }}
                />
                    </div>
        );
      }

    }

export default Graph    