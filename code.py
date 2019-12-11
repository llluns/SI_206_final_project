import requests
import json
import tweepy  
import sqlite3
import csv
import os 
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from PIL import Image
from sqlite3 import Error


# Fill these in in the twitter_info.py file
consumer_key =  "51KkHDO8Ewqr6lIo5yQEP83Ro"
consumer_secret = "aJhvU5Zxs76phrk2yfm8XaznefTJpmot1s6kakR8FhxWi6uzXn"
access_token = "1445359550-vvfBG1xSFNz8bLw7zx36CkbZvN2Mh6UqyohDQT7"
access_token_secret = "NlAwhaKRyTc7P0O75cWn7gBcQQTLCcx4Pk4DyfFu1Kokk"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def get_tweets(consumer_key,consumer_secret,access_token_secret,access_token, query): #already rate limited to 20
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # a search example 
    results = api.search(q=query)
    contents= json.dumps(results)
    return results

def extract_info(results): 
    data=[]
    for status in results['statuses']:
        tweet= status["text"]
        print(tweet)
        name= status['user']['name']
        username=status['user']["screen_name"]
        location=status['user']['location']
        followers=status['user']['followers_count']
        mutuals=status['user']['friends_count']
        when= status['created_at']
        tweet_id=status['id']
        coords=status['coordinates']
        geo=status['geo']
        d={'id':tweet_id,"followers":followers, "tweet": tweet}
        # output
        data.append(d)
    return data 


def write_to_twitter_db(data, num=15): #num is what will restrict how much is written at a time
    conn=sqlite3.connect('/Users/Lauren/Desktop/FinalProject/Twitter.db')
    twitter=conn.cursor() 
    twitter.execute('CREATE TABLE IF NOT EXISTS Tweets (Id INTEGER, Tweet TEXT)')
    twitter.execute('CREATE TABLE IF NOT EXISTS Followers (Id INTEGER, Followers INTEGER)')

    for i in range(0,num): #rate limited
        info=data[i]
        tweet_id=info['id']
        followers=info['followers']
        tweet=info['tweet']
        twitter.execute('INSERT INTO Tweets (Id, Tweet) VALUES (?, ?)',(tweet_id, tweet))
        twitter.execute('INSERT INTO Followers (Id, Followers) VALUES (?, ?)', (tweet_id, followers))
    conn.commit()

###NEED TO FIGURE OUT HOW TO AVOID DUPLICATES 

def retrieve_tweets_from_db():
    conn=sqlite3.connect('/Users/Lauren/Desktop/FinalProject/Twitter.db')
    twitter=conn.cursor() 
    twitter.execute('SELECT Tweets.Id, Tweets.Tweet, Followers.Followers from Tweets INNER JOIN Followers ON Tweets.Id =Followers.Id')
    #twitter.execute('SELECT * from Tweets')
    tweets=[]
    for row in twitter:
        tweets.append(row)
    twitter.close()
    return tweets

def get_sentiment_words():
    filename="sentiment_words.csv"
    root_path = os.path.dirname(os.path.abspath(__file__)) + '/' + filename
    file_obj=open(root_path, 'r')
    file_data = file_obj.readlines()

    sentiment={}
    for line in file_data[1:len(file_data)]:
        parts=line.split(",")
        combined=parts[0]
        score=(parts[1])
        both=combined.split('#')
        part_of_speech=both[1]
        word=both[0]
        score= score.strip('\n')
        score=float(score)
        sentiment[word]=score
    return sentiment

def analyze_twitter():  
    data=retrieve_tweets_from_db()
    sentiment=get_sentiment_words()
    results=[]
    for tup in data:
        Id=tup[0]
        text=tup[1]
        followers=tup[2]
        total=0
        for word in text.split():  #turning tweet into words
            if len(word)>20:      #not taking into account words longer than 20 words
                pass
            else:
                if word in sentiment:  #only taking words in the dictionary
                    total+= sentiment[word]  #summing, NOT averaging 
        info=(total, followers, text)
        results.append(info)
    return results

def get_top_words():
    data=retrieve_tweets_from_db()
    sentiment=get_sentiment_words()
    words={}
    for tup in data:
        text=tup[1]
        followers=tup[2]
        for word in text.split():  #turning tweet into words
            if len(word)>20:      #not taking into account words longer than 20 words
                pass
            else:
                if word in sentiment:  #only taking words in the dictionary
                    if word in words:
                        words[word]['frequency']+=1
                    else:
                        words[word]= {'score':sentiment[word], 'frequency':1}
    data_list=[]
    for word in list(words.keys()):
        score=words[word]['score']
        freq= words[word]['frequency']
        data_list.append((word, score, freq))
    return data_list

def plot_twitter_bar():
    data=get_top_words()
    top=sorted(data, key=lambda x: x[2], reverse=True)
    yep=[]
    for tup in top:
        if len(tup[0])>=4:
            yep.append(tup)
    top3=yep[0:3]
    words=[]
    scores=[]
    freqs=[]
    for word in top3:
        words.append(word[0])
        scores.append(word[1])
        freqs.append(word[2])
    plt.figure(1, figsize= (9, 3))
    plt.tight_layout()
    plt.axes(xlabel ='Word', ylabel="Frequency")
    plt.bar([1,2,3], freqs, color= ["pink", "gold", "deepskyblue"], tick_label=words)
    plt.suptitle('3 Most Frequent Words & Their Sentiment Scores')    
    for i in range(1,4):
            plt.text(i-.1, 1, scores[i-1] )
    plt.show()
    plt.xticks(rotation=90) 
    

def word_cloud_twitter():
    filename="images.png"
    root_path = os.path.dirname(os.path.abspath(__file__)) + '/' + filename
    data=get_top_words()
    top=sorted(data, key=lambda x: x[2], reverse=True)
    yep=[]
    for tup in top:
        if len(tup[0])>=4:
            yep.append(tup)
    top3=yep
    words={}
    for word in top3:
        words[word[0]]=(word[2])
    football_mask = np.array(Image.open(root_path))

    wc = WordCloud(background_color="white", max_words=100, mask=football_mask)
    # generate word cloud
    wc.generate_from_frequencies(words)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()



#writes the contents to a file
def write_to_file(filename):
    col_names= ["Total Sentiment Score", "Follower Count", "Tweet"]
    with open(filename, mode='w') as file:
        f = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.writerow(col_names)
        for line in analyze_twitter():
            f.writerow(line)
    file.close()
    print('The data you have just saved to {} is: '.format(filename))
    print(analyze_twitter())




def get_data():
    response = requests.get("https://api.collegefootballdata.com/rankings?year=2019&seasonType=regular")

    results = response.json()
    #print(json.dumps(results))
    return results

def input_week(week):
    input_week = week
    
    if week >=8 and week < 10:
        week = week-9
    elif week <=7 and week >=1:
        week = week + 3
    elif week <=16 and week >11:
        week = week -1
    else:
        week = week
    #Checking and Showing which Weeks data we are looking at
    print ("2019 College Football Rankings (Week:{})".format(input_week))
    return week

def extract_info_from_week():
#Getting all data within inputted week
    results=get_data()
    week=input_week(4)
    week_data=results[week]

#Getting all the data within the polls part of the week
    all_poll_data=week_data['polls']
    num_of_polls_in_week = len(all_poll_data)
    print("Polls:{}".format(num_of_polls_in_week))
    
    giant_data = []
    count = 0

#Looking at each individual poll inside the poll section of the week
    for i in range(0,len(all_poll_data)):
        count +=1
        polldata=all_poll_data[i]
#itterating through each individual poll to extract and assign data values and also appending that data to a giant list
        if i == 0:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname
                giant_data.append((id_name, school, rank, conference))
        if i == 1:
            pollname = polldata["poll"]
            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname
                giant_data.append((id_name, school, rank, conference))
        if i == 2:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname
                giant_data.append((id_name, school, rank, conference))
        if i == 3:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname
                giant_data.append((id_name, school, rank, conference))
        if i == 4:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname
                giant_data.append((id_name, school, rank, conference))

    return giant_data


def write_to_football_Table1():
    conn=sqlite3.connect('/Users/Lauren/Desktop/FinalProject/Football.db')
    football=conn.cursor() 

    giantdata = extract_info_from_week()
    football.execute('CREATE TABLE IF NOT EXISTS Table1 (id_name TEXT, school TEXT, rank INTEGER)')
    itemsInDB = football.execute("SELECT * FROM Table1")
    itemsInDB = football.fetchall()
    itemsInDB = len(itemsInDB)
    if itemsInDB == 0:
        for i in giantdata[:20]:
            id_name = i[0]
            school=i[1]
            rank=i[2]
            football.execute('INSERT INTO Table1 (id_name, school, rank) VALUES (?, ?, ?)', (id_name, school, rank))
    if itemsInDB == 20:
        for i in giantdata[20:40]:
            id_name = i[0]
            school=i[1]
            rank=i[2]
            football.execute('INSERT INTO Table1 (id_name, school, rank) VALUES (?, ?, ?)', (id_name, school, rank))
    if itemsInDB == 40:
        for i in giantdata[40:60]:
            id_name = i[0]
            school=i[1]
            rank=i[2]
            football.execute('INSERT INTO Table1 (id_name, school, rank) VALUES (?, ?, ?)', (id_name, school, rank))
    if itemsInDB == 60:
        for i in giantdata[60:80]:
            id_name = i[0]
            school=i[1]
            rank=i[2]
            football.execute('INSERT INTO Table1 (id_name, school, rank) VALUES (?, ?, ?)', (id_name, school, rank))
    if itemsInDB == 80:
        for i in giantdata[80:100]:
            id_name = i[0]
            school=i[1]
            rank=i[2]
            football.execute('INSERT INTO Table1 (id_name, school, rank) VALUES (?, ?, ?)', (id_name, school, rank))
    print("Currently there are {} items in Table1".format(itemsInDB +20))

    conn.commit()
    conn.close()

def get_avg_rates():
    conn=sqlite3.connect('/Users/Lauren/Desktop/FinalProject/Football.db')
    football=conn.cursor() 

    results = football.execute("SELECT school, AVG(rank) FROM Table1 GROUP BY school")
    results = football.fetchall()
    school_and_rank = {}
    for item in results:
        school_and_rank[item[0]] = item[1]

    return school_and_rank


#writes the contents to a file
def write_to_file2(filename):
    col_names= ["College Team", "Average Ranking"]
    with open(filename, mode='w') as file:
        f = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f.writerow(col_names)
    for line in get_avg_rates():
            f.writerow(line)
    file.close()
    print('The data you have just saved to {} is: '.format(filename))




def set_Table2():
    giantdata = extract_info_from_week()
    schools_and_conf = []
    table2_data = []
    for x in giantdata:
        school = x[1]
        conf = x[3]
        schools_and_conf.append((school,conf))

    for x in schools_and_conf:
        if x in table2_data:
            None
        else:
            table2_data.append(x)
    return table2_data



def find_conference(input):
    data = set_Table2()
    for i in data:
        if i[1] == input:
            return i[1]
        return "No Conference"



def find_school(input):
    data = set_Table2()
    for i in data:
        if i[0] == input:
            return i[0]
        return "School not Found"


def find_avg_rank(input):
    data = get_avg_rates()
    for school, rank in data.items(): 
        if rank == input: 
            return input 
        return "No rank data available"

def write_to_football_Table2():
    conn=sqlite3.connect('/Users/Lauren/Desktop/FinalProject/Football.db')
    football=conn.cursor() 
    data_tups = set_Table2()
    football.execute('CREATE TABLE IF NOT EXISTS Table2 (school TEXT, conference TEXT)')
    itemsInDB2 = football.execute("SELECT * FROM Table2")
    itemsInDB2 = football.fetchall()
    itemsInDB2 = len(itemsInDB2)
    if itemsInDB2 == 0:
        for i in data_tups[:20]:
            school=i[0]
            conference=i[1]
            football.execute('INSERT INTO Table2 (school, conference) VALUES (?, ?)', (school, conference))
    if itemsInDB2 == 20:
        for i in data_tups[20:40]:
            school=i[0]
            conference=i[1]
            football.execute('INSERT INTO Table2 (school, conference) VALUES (?, ?)', (school, conference))
    if itemsInDB2 == 40:
        for i in data_tups[40:60]:
            school=i[0]
            conference=i[1]
            football.execute('INSERT INTO Table2 (school, conference) VALUES (?, ?)', (school, conference))
    if itemsInDB2 == 60:
        for i in data_tups[60:80]:
            school=i[0]
            conference=i[1]
            football.execute('INSERT INTO Table2 (school, conference) VALUES (?, ?)', (school, conference))
    if itemsInDB2 == 80:
        for i in data_tups[80:100]:
            school=i[0]
            conference=i[1]
            football.execute('INSERT INTO Table2 (school, conference) VALUES (?, ?)', (school, conference))

    print("Currently there are {} items in Table2".format(itemsInDB2 + 20))
    conn.commit()
    conn.close()


def data_vis_Table1():
    data = get_avg_rates()
    ranks = list(data.values())
    schools = list(data.keys())
    lst=[]
    for i in range(0,len(ranks)):
        lst.append((schools[i],ranks[i]))
    sort=sorted(lst, key= lambda x: x[1], reverse=True)
    sorted_ranks=[]
    sorted_schools=[]
    for tup in sort:
        sorted_ranks.append(tup[1])
        sorted_schools.append(tup[0])


    fig = plt.figure()
    fig.subplots_adjust(top=0.8)
    ax1 = fig.add_subplot()


    plt.figure(1, figsize= (9, 3))
    plt.tight_layout()
    rainbow=["red","orange",'yellow','green','blue','purple']
    plt.barh(sorted_schools, sorted_ranks, color=rainbow)
    plt.suptitle('College Teams and Average Rankings in 2019')
    ax1.set_ylabel('College Teams')
    ax1.set_xlabel("Ranking")
    plt.show()
    plt.tight_layout()
    




def main():
    #TWITTER 
    try:
        schools=list(get_avg_rates().keys())
        print (schools)

        
    print("Please type a school from the list above. Please make sure to match spelling and capitalization. ")
    print("If no schools are printed, please run the code several more times to allow the database to update.")
    query= input("Please enter school here: ")
    results=get_tweets(consumer_key,consumer_secret,access_token_secret,access_token, query)
    data=(extract_info(results))
    write_to_twitter_db(data)
    #FOOTBALL
    write_to_football_Table1()
    write_to_football_Table2()
    #OUTPUT
    school= find_school(query)
    conference= find_conference(query)
    rank=  find_avg_rank(query)
    print("{} is in the {} conference and is ranked {}".format(school, conference, rank))
    #DISPLAY VISUALIZATOINS
    data_vis_Table1()
    plot_twitter_bar()
    word_cloud_twitter()
    #WRITE FILE
    write_to_file( "Twitter_results.csv" )
    write_to_file2( "Avg_Rankings.csv" )
 

print(schools)


