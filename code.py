import requests
import json
import tweepy 			# need to pip install tweepy

# Fill these in in the twitter_info.py file
consumer_key =  "51KkHDO8Ewqr6lIo5yQEP83Ro"
consumer_secret = "aJhvU5Zxs76phrk2yfm8XaznefTJpmot1s6kakR8FhxWi6uzXn"
access_token = "1445359550-vvfBG1xSFNz8bLw7zx36CkbZvN2Mh6UqyohDQT7"
access_token_secret = "NlAwhaKRyTc7P0O75cWn7gBcQQTLCcx4Pk4DyfFu1Kokk"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


def get_tweets(consumer_key,consumer_secret,access_token_secret,access_token, query):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # a search example
    results = api.search(q=query)
    contents= json.dumps(results)
    return results

def extract_info(results):
    users_tweets={}
    tweets=[]
    extra={}
    for status in results['statuses']:
        tweet= status["text"]
        print(tweet)
        name= status['user']['name']
        username=status['user']["screen_name"]
        location=status['user']['location']
        followers=status['user']['followers_count']
        mutuals=status['user']['friends_count']
        when= status['created_at']
        coords=status['coordinates']
        geo=status['geo']
        words={}
        words_list=tweet.split()
        for word in words_list: 
            if word in words:
                words[word]+=1
            else:
        
                words[word]=1
        #simple output
        users_tweets[name]=tweets
        tweets.append(tweet)

        #extra output
        extra[name]={'name':name, 'username':username, 'location':location, "followers":followers, 'mutuals':mutuals, 'when':when , 'geo': geo, 'coords':coords,'word_freq':words}
        return tweets 

def calc_word_frequencies(tweet):
    words={}
    for word in tweet.split():
        if len(word)<20: 
            if word in words:
                words[word]+=1
            else:
                words[word]=1

def create_db(databasename):
    CREATE DATABASE databasename;

def create_table(databasename, table_name):
    CREATE TABLE table_name ()


def write_to_db(data):



#writes the contents to a file
def write_to_file(data, filename):
    f = open(filename, "w")
    f.write(json.dumps(data))
    f.close()
    print('The data you have just saved to {} is:'.format(filename))
    print(data)


def main():
    create_db('Tweets')
    create_table('Username' TEXT, "Tweet" TEXT)
    create_table('Username' TEXT, "Followers" INT)
