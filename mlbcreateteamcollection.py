import requests
import json
import pymongo
#Looks up the 40 man roster for the team
#response = requests.get("http://lookup-service-prod.mlb.com/json/named.roster_team_alltime.bam?start_season=2020&end_season=2021&team_id=121")
#Getting a list of all active teams
#Store the list of all teams in a local database
#https://appac.github.io/mlb-data-api-docs/#team-data-list-teams-get

#Compile a list of total players on the team
#Store players in a database
#Create custom metrics for each player based on batting average hitting average fielding
#Complie an list of team ranking based on who has the best players
#Set up a job to have the list automatically update everynight
#Send an alert if there's a ton of movement
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
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
#x = mycol.insert_many(teamsdictList)
#print(x.inserted_ids)
#Store the list of all teams in a local database

#Compile a list of total players on the team
#Store players in a database
#Create custom metrics for each player based on batting average hitting average fielding
#Complie an list of team ranking based on who has the best players
#Set up a job to have the list automatically update everynight
#Send an alert if there's a ton of movement