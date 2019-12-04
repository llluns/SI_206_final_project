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

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# a search example
results = api.search(q="soap")
print(type(results), "is the type of the results variable") 
contents= json.dumps(results)

## OK, it's a dictionary. What are its keys?
print("________________________")

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
    #simple
    users_tweets[name]=tweets
    tweets.append(tweet)

    #extra 
    extra[name]={'name':name, 'username':username, 'location':location, "followers":followers, 'mutuals':mutuals, 'when':when , 'geo': geo, 'coords':coords,'word_freq':words}


#writes the contents to a file

f = open("twitterdata{}.txt", "w".format())
f.write(json.dumps(extra))
f.close()
print(extra)


#______________________________________________________________________________________
