# MLBHittingRankings
Updated ranking of the best hitters in the MLB 

Uses mlb stats pulled using the api https://appac.github.io/mlb-data-api-docs/#team-data-list-teams-get

1. mlbcreateteamcollection.py gets a list of active MLB teams and stores it to a mongodb database for future use 
2. mlbcreateplayercollection.py get a list of active players for each of the teams found in the database and stores it in a new players collection 
3. mlbupdateplayerhitting.py gets an avg stats from all the seasons played on the current team they are playing for. Does not count seaasons where the player may have been out for injury or if there is a whole in the data set
4. mlbcalcranking.py uses the stat metrics to calculate an overall score and using that overall score generates a ranking for each player in the database and stores new ranking to players collection 
5. mlbgettopplay.py this is the main program that you will run after building the datasets and calculating the metrics for the top players. This program currently returns a list of the top 200 players.
