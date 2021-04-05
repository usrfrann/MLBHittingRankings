import requests
import json
import pymongo
import datetime

currDate = datetime.datetime.now()
mongoClient = pymongo.MongoClient("mongodb://<edit>/")
mydb = mongoClient["mlbdatabase"]
playersCol = mydb["players"]
playerList = []
hittingUpdateDict = []
myquery = {}
mydoc = playersCol.find(myquery,{"teamcode":0,"teamid":0, "timeidObj": 0})
for x in mydoc:
    playerList.append(x)

for player in playerList:
    startdate = datetime.datetime.strptime((player['start_date']), '%Y-%m-%dT%H:%M:%S')
    gidpAvg = 0
    gidpTotal = 0
    sacTotal = 0
    sacAvg = 0
    npTotal = 0
    hgndTotal,hgndAvg = 0,0
    tbTotal,tbAvg = 0,0
    havgTotal,havgAvg = 0,0
    slgTotal,slgAvg = 0,0
    soTotal,soAvg = 0,0
    ppaTotal,ppaAvg = 0,0
    goTotal,goAvg = 0,0
    hrTotal,hrAvg = 0,0
    rbiTotal,rbiAvg = 0,0
    babipTotal,babipAvg = 0,0
    rTotal,rAvg = 0,0
    aoTotal,aoAvg = 0,0
    abTotal,abAvg = 0,0

    keyErrors = 0
    for date in range(startdate.year,currDate.year + 1):
        url = "http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season="+str(str(date))+"&player_id="+str(str(player['playerid']))
        print(url)
        #
        try:
            response = requests.get("http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season="+str(date)+"&player_id="+str(player['playerid']))
            hitting_dict = response.json()
            hitstruct = hitting_dict['sport_hitting_tm']['queryResults']['row']
            print(hitting_dict)
            try:
                gidpTotal += float(hitstruct['gidp'])
                sacTotal += float(hitstruct['sac'])
                npTotal += float(hitstruct['np'])
                hgndTotal += float(hitstruct['hgnd'])
                tbTotal += float(hitstruct['tb'])
                havgTotal += float(hitstruct['avg'])
                slgTotal += float(hitstruct['slg'])
                soTotal += float(hitstruct['so'])
                ppaTotal += float(hitstruct['ppa'])
                goTotal += float(hitstruct['go'])
                hrTotal += float(hitstruct['hr'])
                rbiTotal += float(hitstruct['rbi'])
                babipTotal += float(hitstruct['babip'])
                rTotal += float(hitstruct['r'])
                aoTotal += float(hitstruct['ao'])
                abTotal += float(hitstruct['ab'])
                totalTimePasted = abs(((startdate.year-1)-date))
                print("Total time passed", totalTimePasted)
            except ValueError:
                continue
            except TypeError:
                continue
            #gidpAvg = gidpTotal / totalTimePasted
        except KeyError:
            keyErrors += 1
            continue
        gidpAvg = gidpTotal / (totalTimePasted - keyErrors)
        sacAvg = sacTotal / (totalTimePasted - keyErrors)
        hgndAvg = hgndTotal / (totalTimePasted - keyErrors)
        tbAvg = tbTotal / (totalTimePasted - keyErrors)
        havgAvg = havgTotal / (totalTimePasted - keyErrors)
        slgAvg = slgTotal / (totalTimePasted - keyErrors)
        soAvg = soTotal / (totalTimePasted - keyErrors)
        ppaAvg = ppaTotal / (totalTimePasted - keyErrors)
        goAvg = goTotal / (totalTimePasted - keyErrors)
        hrAvg = hrTotal / (totalTimePasted - keyErrors)
        rbiAvg = rbiTotal / (totalTimePasted - keyErrors)
        babipAvg = babipTotal / (totalTimePasted - keyErrors)
        rAvg = rTotal / (totalTimePasted - keyErrors)
        aoAvg = aoTotal / (totalTimePasted - keyErrors)
        abAvg = abTotal / (totalTimePasted - keyErrors)
        #gdpAvg = (int(hitstruct['gidp']) + gpdAvg) / (currDate.year - date)
    hittingUpdateDict.append({"playerid":str(player['playerid']),"gidp":gidpAvg,"sac":sacAvg,"np":npTotal,"hgnd":hgndAvg,"tb":tbAvg,"avg":havgAvg,"slg":slgAvg,"so":soAvg, "ppa":ppaAvg, "so":soAvg,"ppa":ppaAvg,"go":goAvg,"hr":hrAvg,"rbi":rbiAvg,"babip": babipAvg, "r":rAvg,"ao":aoAvg,"ab":abTotal})


for x in hittingUpdateDict:
    query = {"playerid": x['playerid']}
    setvalue = {"$set": x}
    print(x)
    x = playersCol.update_one(query,setvalue)
    print(x.modified_count, "documents updated.")
