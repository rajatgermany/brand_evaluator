import React, {Component} from 'react';
import Plot from 'react-plotly.js';

class TweetViewer extends Component {
    constructor(props) {
        super(props);
        this.state = {
          query: '',
          sentiment: '',
          showTweet: false
        }
        this.showTweets = this.showTeets.bind(this)
      }

      showTeets() {
        this.setState({
            showTweet: !this.state.showTweet
          });
      }
      render() {
          if (this.props.tweets === "") {
            return null
        }
        return (
            <div>
            <button onClick ={this.showTweets}>Show Tweets</button>
            {
                this.state.showTweet && this.props.tweets.map(tweet => <div> {tweet.text} </div>)} 
            }
            </div>
        )
      }

    }

export default TweetViewer    