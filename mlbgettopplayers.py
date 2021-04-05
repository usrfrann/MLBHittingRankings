import json
import pymongo
import re

mongoClient = pymongo.MongoClient("mongodb://<edit>/")
mydb = mongoClient["mlbdatabase"]
playersCol = mydb["players"]
playerList = []
playerRanks = []
regx = re.compile("^[0-1][0-9][0-9]",re.IGNORECASE)
for x in range(0,200):
    myquery = {"ranking": x}

    mydoc = playersCol.find(myquery,{"name":1,"ranking":1})

    for x in mydoc:
        playerList.append(x)

print(playerList)
