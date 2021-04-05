import requests
import json
import pymongo
mongoClient = pymongo.MongoClient("mongodb://<edit>/")
mydb = mongoClient["mlbdatabase"]
playersCol = mydb["players"]
teamCol = mydb["teams"]
teamsList = []
position = []
name = []
teamcode = []
player_id = []
teamid = []
startdate = []
playerDictList = []
idList = []
mydoc = teamCol.find({},{"_id":0,"venue":0,"frachise":0, "city": 0})
for x in mydoc:
    dict = eval(str(x))
    teamsList.append(dict)


for team in teamsList:
    #print(team['teamid'])
    myquery = {"teamid" : team['teamid']}
    doc = teamCol.find(myquery,{"_id":1})
    objId = 0
    for x in doc:
        objId = x
    print(objId)
    response = requests.get("http://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id="+str(team['teamid']))
    roster_dict = response.json()
    if int(roster_dict["roster_40"]["queryResults"]["totalSize"]) == 0:
        continue
    player_dict = roster_dict["roster_40"]["queryResults"]["row"]
    for i in range(0,int(roster_dict["roster_40"]["queryResults"]["totalSize"])):
        playerDictList.append({'position':player_dict[i]["position_txt"], 'name':player_dict[i]["name_display_first_last"], 'teamcode':player_dict[i]["team_code"], 'playerid': player_dict[i]["player_id"], 'teamid': player_dict[i]["team_id"],'teamidObj': objId['_id'], 'start_date':player_dict[i]["start_date"]})

x = playersCol.insert_many(playerDictList)
