import requests
import json
import tweepy 			
import sqlite3
import matplotlib.pyplot as plt

import sqlite3
from sqlite3 import Error

 

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


    # print("motherdata")
    # print(len(giant_data))
    # print(giant_data)
    return giant_data



def write_to_football_Table1():
    conn=sqlite3.connect('/Users/shrinalipatel/Desktop/collegefootball.sqlite')
    football=conn.cursor() 

    #currIds=get_ids_from_db()

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
    conn=sqlite3.connect('/Users/shrinalipatel/Desktop/collegefootball.sqlite')
    football=conn.cursor() 

    results = football.execute("SELECT school, AVG(rank) FROM Table1 GROUP BY school")
    results = football.fetchall()
    school_and_rank = {}
    for item in results:
        school_and_rank[item[0]] = item[1]

    return school_and_rank




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


def write_to_football_Table2():
    conn=sqlite3.connect('/Users/shrinalipatel/Desktop/collegefootball.sqlite')
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
    conn=sqlite3.connect('/Users/shrinalipatel/Desktop/collegefootball.sqlite')

    get_data()
    input_week(4)
    extract_info_from_week()
    write_to_football_Table1()
    get_avg_rates()
    
    set_Table2()
    write_to_football_Table2()
    data_vis_Table1()
    print("______________________code end___________________")
main()



