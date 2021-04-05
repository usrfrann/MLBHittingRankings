import json
import pymongo

mongoClient = pymongo.MongoClient("mongodb://<edit>")
mydb = mongoClient["mlbdatabase"]
playersCol = mydb["players"]
playerList = []
playerRanks = []
myquery = {}
mydoc = playersCol.find(myquery,{"teamcode":0,"teamid":0, "timeidObj": 0})
rankingScore = 0
for x in mydoc:
    playerList.append(x)

for player in playerList:
    rankingScore = (player['ab'] - player['ao'] - (player['gidp'] * 10) - player['go'] + (player['hgnd'] * 3) + (player['hr'] * 30) + (player['r'] * 20) + (player['rbi'] * 10) - (player['sac'] * 5) - (player['so'] * 2)) * player['avg']
    print(rankingScore)
    if rankingScore == 0:
        continue
    playerRanks.append({'playerid':player['playerid'],'rankingS': rankingScore})
print(playerList)
print("The list is now sorted")
sortedPlayerRank= sorted(playerRanks, key = lambda i: i['rankingS'], reverse = True)

for idx,prank in enumerate(sortedPlayerRank):
    query = {"playerid": prank['playerid']}
    setVar = {"ranking": idx, "rankingScore": prank['rankingS']}
    setvalue = {"$set": setVar}
    x = playersCol.update_one(query,setvalue)
