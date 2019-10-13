import React, {Component} from 'react';
import TweetService from "../services/TweetsService";
import Graph from './graph.js'
import TweetViewer from './tweetviewer.js'
import brand_tweets_response from '../helpers/normalizers'

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
          tweets: ''
        };
    
        this.handleSuccess = this.handleSuccess.bind(this)
        this.handleError = this.handleError.bind(this)
      }
      
      updateInputValue(evt) {
        this.setState({
          brand: evt.target.value
        });
      }

      handleSuccess(response){
        this.setState({
            tweets: brand_tweets_response(response)
          });
      }

      handleError(response){
        console.log(response)
      }

      handleClick() {
        const sentiment = TweetService.getsentiment(this.state.brand, this.handleSuccess, this.handleError)

      }

      render() {
        return (
          <div>
            <input onChange={evt => this.updateInputValue(evt)}/>
            <button onClick ={() => this.handleClick()}>Submit</button>
            <Graph tweets = {this.state.tweets}/>
          </div>
        );
      }
    
}

export default Home;
