import requests
import json
import tweepy 			
import sqlite3


import sqlite3
from sqlite3 import Error

 

def get_data():
    response = requests.get("https://api.collegefootballdata.com/rankings?year=2019&seasonType=regular")

    results = response.json()
    #print(json.dumps(results))
    return results

def extract_info (results, week):
    print(week)

    if week >=8 and week < 10:
        week = week-9
    elif week <=7 and week >=1:
        week = week + 3
    else:
        week = week

#Getting all data within inputted week

    week_data=results[week]
    print("week data")
    print(week_data)

#Getting all the data within the polls part of the week

    all_poll_data=week_data['polls']
    print(" All poll data_____________")
    print(all_poll_data)
    print("length")
    print(len(all_poll_data))

    giant_data = []
    count = 0

#Looking at each individual poll inside the poll section of the week
    for i in range(0,len(all_poll_data)):
        count +=1
        print("Poll Number:_________________" + str(count))

        polldata=all_poll_data[i]
        print("Poll Data___________________:")

        print(polldata)




#itterating through each individual poll to extract and assign data values and also appending that data to a giant list
        if i == 0:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname

                if id_name in giant_data:
                    None
                else:
                    giant_data.append((id_name, school, rank, conference))

        if i == 1:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname

                if id_name in giant_data:
                    None
                else:
                    giant_data.append((id_name, school, rank, conference))

        if i == 2:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname

                if id_name in giant_data:
                    None
                else:
                    giant_data.append((id_name, school, rank, conference))

        if i == 3:
            pollname = polldata["poll"]

            for item in polldata["ranks"]:
                school = item["school"]
                rank = item["rank"]
                conference = item["conference"]
                id_name =  school + "_" + pollname

                if id_name in giant_data:
                    None
                else:
                    giant_data.append((id_name, school, rank, conference))

    print("motherdata")
    print(len(giant_data))
    print(giant_data)
    return giant_data

#Setting up table

def set_football_db_one():
    conn=sqlite3.connect('/Users/shrinalipatel/Desktop/Football.sqlite')
    football=conn.cursor() 
    football.execute('DROP TABLE IF EXISTS Table1')
    football.execute('CREATE TABLE Table1 (id_name TEXT, school TEXT, rank INTEGER)')



#Writing to Table 1


def write_to_football_db():
    conn=sqlite3.connect('/Users/shrinalipatel/Desktop/Football.sqlite')
    football=conn.cursor() 
    results = get_data()
    giantdata = extract_info(results, 3)
    football.execute('SELECT id_name FROM Table1')
    currIds=[]      #fetch list of IDs
    for Id in football:
        currIds.append(Id)
    count=0
    while True:
        for i in giantdata: 
            id_name = i[0]
            school=i[1]
            rank=i[2]
            if id_name in currIds:
                pass
            else:
                football.execute('INSERT INTO Table1 (id_name, school, rank) VALUES (?, ?, ?)', (id_name, school, rank))
                count+=1
            if count ==20:
                break
    football.commit()
    football.close()














def main():
    yasss=get_data()
    alldata=(extract_info(yasss, week=3))


    conn=sqlite3.connect('/Users/shrinalipatel/Desktop/Football.sqlite')


set_football_db_one()
write_to_football_db()
