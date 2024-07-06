from time import sleep
import pandas as pd
from pymongo import MongoClient
import os
import warnings
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(parent_dir)


from config.config import config

# Suppress all warnings
warnings.filterwarnings("ignore")

#This page pull data from TSV file and push to Mongo DB using Spark SQL
def start_streaming():
        try:
            
            #get current folder path
            current_directory = os.getcwd()
            
            print("Reading files from the TSV file")
            #Load the TSV file into a DataFrame
            tsv_data = pd.read_csv(current_directory+r"\datasets\Correct_twitter_201904.tsv", sep='\t', header=0, dtype=str)
            
            if_database_exists('localhost', 27017, config['mongodb']['username'], config['mongodb']['password'], 'Twitter_Tweets', 'Tweets')
            
            #Writing the data to database
            host = 'localhost'
            port = 27017
            username = config['mongodb']['username']
            password = config['mongodb']['password']
            database_name = 'Twitter_Tweets'
            collection_name = 'Tweets'

            # Create a MongoDB client
            client = MongoClient(host, port, username=username, password=password)

            # Access the database and collection
            db = client[database_name]
            collection = db[collection_name]

            # Convert the DataFrame to a list of dictionaries and insert into MongoDB
            data_dict = tsv_data.to_dict("records")
            collection.insert_many(data_dict)


            # Clean up resources
            client.close()
            
            print("Data loaded successfully")
            

        except Exception as e:
            print(f'Exception encountered: {e}. Retrying in 10 seconds')
            sleep(10)

def if_database_exists(host, port, username, password, database_name, collection_name):
    
    #Ensures that the specified MongoDB database and collection exist.Creates them if they do not exist with an initial document in the collection.
    client = MongoClient(host, port, username=username, password=password)
    db_list = client.list_database_names()

    if database_name in db_list:
        print(f"Database '{database_name}' already exists.")
    else:
        # Create the database by creating a collection in it
        print(f"Database '{database_name}' not found, creating now...")
        db = client[database_name]
        collection = db[collection_name]
        print(f"Database '{database_name}' and collection '{collection_name}' created.")

    # Clean up resources
    client.close()
    



if __name__ == "__main__":
    
    start_streaming()
