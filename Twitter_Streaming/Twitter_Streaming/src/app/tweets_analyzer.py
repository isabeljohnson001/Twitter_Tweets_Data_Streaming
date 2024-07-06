from flask import jsonify
import pandas as pd
import json
from itertools import groupby
from collections import defaultdict
from datetime import datetime, timedelta

def df_to_json(df):
    return df.to_json(orient='records')

class Tweets_Analyser:
    def __init__(self, tweets_list):
        self.tweets_list = tweets_list

    def query_term(self, term):
        # filter the tweets that contain that term
        df = pd.DataFrame(self.tweets_list)

        # Convert the 'likes' column to integer type
        df['like_count'] = df['like_count'].astype(int)

        # Get the top 10 tweets with the most likes
        top_10_tweets = df.nlargest(10, 'like_count')
        
        # Group by the 'created_at' column and count the number of tweets per day
        tweets_per_day = df.groupby(df['created_at'])['id'].count()

        # Convert the Timestamp to string in the format 'YYYY-MM-DD HH:MM:SS'
        #tweets_per_day = {key.strftime('%Y-%m-%d %H:%M:%S'): value for key, value in tweets_per_day.items()}
        formatted_tweets_per_day = {
        datetime.strptime(key, '%Y-%m-%d %H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'): value
            for key, value in tweets_per_day.items()
        }
        # Get the number of tweets per day
        tweets_per_day=df.groupby(df['created_at'])['id'].count()
        # Convert Timestamp to string in the format 'YYYY-MM-DD HH:MM:SS'
        #tweets_per_day = {key.strftime('%Y-%m-%d %H:%M:%S'): value for key, value in tweets_per_day.items()}
        tweets_per_day = {datetime.strptime(key, '%Y-%m-%d %H:%M:%S%z'): value for key, value in tweets_per_day.items()}
        # Get the average number of likes
        avg_likes = df['like_count'].mean()

        # Get the number of tweets per hour
        tweets_per_hours=df.groupby(df['created_at'])['id'].count()
        # Convert Timestamp to string in the format 'HH:MM:SS'
        #tweets_per_hour = {key.strftime('%H'): value for key, value in tweets_per_hour.items()}
        # Convert string keys to datetime objects and aggregate by hour
        tweets_per_hour = {}
        for key, value in tweets_per_hours.items():
            hour = datetime.strptime(key, '%Y-%m-%d %H:%M:%S%z').strftime('%H')
            if hour in tweets_per_hour:
                tweets_per_hour[hour] += value
            else:
                tweets_per_hour[hour] = value

        tweets_per_week = defaultdict(int)
        for key, value in formatted_tweets_per_day.items():
            date = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
            day_name = date.strftime('%A')  # Get the full day name
            tweets_per_week[day_name] += value
        
        
        # Get the number of tweets per month
        tweets_per_month = df.groupby(df['created_at'])['id'].count()
        # Convert the month name to a string in the format 'MMM'
        #tweets_per_month = {key.strftime('%b'): value for key, value in tweets_per_month.items()}
        tweets_per_month = {datetime.strptime(key, '%Y-%m-%d %H:%M:%S%z').strftime('%b'): value for key, value in tweets_per_month.items()}
        
        # Get the top 10 days with the most tweets
        #top_10_days = tweets_per_day.nlargest(10)
        # Convert string keys to datetime objects and group by day
        tweets_by_day = defaultdict(int)
        for key, value in formatted_tweets_per_day.items():
            day = datetime.strptime(key, '%Y-%m-%d %H:%M:%S').date()
            tweets_by_day[day.isoformat()] += value

        # Sort the days by tweet counts and get the top 10
        top_10_days = sorted(tweets_by_day.items(), key=lambda item: item[1], reverse=True)[:10]
        
        # Get the bottom 10 days with the fewest tweets
        bottom_10_days = sorted(tweets_by_day.items(), key=lambda item: item[1], reverse=False)[:10]
       
        # Create a dictionary with the results
        results = {
            'top_10_tweets': top_10_tweets[['id', 'text', 'like_count']].to_dict(orient='records'),
            'tweets_per_day': tweets_by_day,
            'avg_likes': avg_likes,
            'tweets_per_hour': tweets_per_hour,
            'tweets_per_weekday': tweets_per_week,
            'tweets_per_month': tweets_per_month,
            'top_10_days': top_10_days,
            'bottom_10_days': bottom_10_days
        }

        # Convert all DataFrames in the dictionary to JSON serializable format
        json_ready_data = {
            key: df_to_json(value) if isinstance(value, pd.DataFrame) else value for key, value in results.items()
        }

        # Convert the entire dictionary to a JSON string
        json_output = json.dumps(json_ready_data)
        
        # Return the results as a JSON response
        return json_output