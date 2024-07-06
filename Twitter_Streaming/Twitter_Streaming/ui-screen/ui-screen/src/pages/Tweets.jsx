import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import '../App.css';
import getApiUrl from '../apiConfig';



/* This is the tweets results page */
const Tweets = () => {
  const { searchTerm } = useParams();
  const [topTweets, setTopTweets] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const apiUrl = getApiUrl();
      console.log(`Fetching tweets for ${searchTerm} from ${apiUrl}/tweets/${searchTerm}`);
      try {
        const response = await axios.get(`${apiUrl}/tweets/${searchTerm}`);
        let responseData = response.data;

        // Log the entire response data to check its structure
        console.log('Full response data:', responseData);

        // If responseData is a string, parse it as JSON
        if (typeof responseData === 'string') {
          try {
            responseData = JSON.parse(responseData);
            console.log('Parsed response data:', responseData);
          } catch (error) {
            console.error('Failed to parse response data as JSON:', error);
            setTopTweets("Failed to parse response data.");
            setLoading(false);
            return;
          }
        }

        if (responseData) {
          if (responseData.top_10_tweets) {
            const top_10_tweets = responseData.top_10_tweets;

            // Check if top_10_tweets is an array and splits by \n and displays in the ui
            if (Array.isArray(top_10_tweets)) {
              console.log('Top 10 tweets (array):', top_10_tweets);
              const tweetsText = top_10_tweets.map(tweet => tweet.text).join("\n");
              console.log('Top tweets:', tweetsText);
              setTopTweets(tweetsText);
            } 
          } else if (responseData.error) {
            console.error("Response data error:", responseData.error);
            setTopTweets(responseData.error);
          } 
        } 
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch tweets:", error);
        setTopTweets("500 INTERNAL SERVER ERROR: Failed to fetch tweets:");
        setLoading(false);
      }
    };
    fetchData();
  }, [searchTerm]);

  return (
    <div className="tweets-container">
      <h2>Top Tweets for "{searchTerm}"</h2>
      <div className="data-display-container">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <pre className="data-display">{topTweets}</pre>
        )}
      </div>
    </div>
  );
};

export default Tweets;
