import requests
import json
import pymongo
#Looks up the 40 man roster for the team
#Getting a list of all active teams
#Store the list of all teams in a local database

mongoClient = pymongo.MongoClient("mongodb://<edit>/")
mydb = mongoClient["mlbdatabase"]
mycol = mydb["teams"]

response = requests.get("http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&season='2020'")
teamListId = []
venueName = []
franchiseCode = []
city = []
teams_dict = response.json()
teamsdictList = []
team_json_dict = teams_dict['team_all_season']['queryResults']['row']
totalTeam = teams_dict['team_all_season']['queryResults']['totalSize']
#pythonObj = json.loads(teams_dict)
for teamRow in range(0,int(totalTeam)):
    print(teams_dict['team_all_season']['queryResults']['row'][teamRow]['team_id'])
    teamListId.append(teams_dict['team_all_season']['queryResults']['row'][teamRow]['team_id'])
    venueName.append(teams_dict['team_all_season']['queryResults']['row'][teamRow]['venue_name'])
    franchiseCode.append(teams_dict['team_all_season']['queryResults']['row'][teamRow]['franchise_code'])
    city.append(teams_dict['team_all_season']['queryResults']['row'][teamRow]['city'])

for idx in range(0,int(totalTeam)):
    teamsdictList.append({'teamid':teamListId[idx], 'venue':venueName[idx], 'frachise':franchiseCode[idx], 'city': city[idx]})
#data = json.loads(response.read())
print(response.status_code)
x = mycol.insert_many(teamsdictList)
print(x.inserted_ids)
