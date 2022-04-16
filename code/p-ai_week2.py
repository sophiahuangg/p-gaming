import requests, time, os, csv, pandas as pd
from dotenv import load_dotenv

# Summonername=eStarAstral

# Looking at the last fifty matches for eStarAstral

def reqMatchId(puuid, start, count):
  payload = {'start': start, 'count': count}
  load_dotenv() 
  api_key = os.environ.get("Api_Key", None) #Extracting API key from .env file
  payload["api_key"]=api_key
  r=requests.get("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids", params=payload)
  print("Generated URL=", r.url)
  return r.json()

LastFiftyMatches=reqMatchId("kXQNUIvfd1kFPz7TPvqZaI9XRGWt4PFxg33atNJVKi3ufXAi0iCWfmLEc5sUvqdq2iDOxRJbh866hw", "0", "50")
#print("Last Fifty MAtches=", LastFiftyMatches)



# Creating function using requests library to get match url and return a json of matches

def reqMatchData(matchId):
  payload = {}
  load_dotenv() 
  api_key = os.environ.get("Api_Key", None) #Extracting API key from .env file
  payload["api_key"]=api_key
  r = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/'+matchId, params=payload) 
  #print(matchId)
  return r.json()



# creating CSV header (column names)

header = ['matchNum', 'blueKills', 'redKills','blueAssists', 'redAssists', 'blueGold','redGold', 'gameLength', 'OUTCOME']

with open('league_dataset.csv', 'w', encoding='UTF8', newline='') as f:
  writer = csv.writer(f)

  # write the header
  writer.writerow(header)

  matchnum=1

  # iterating through the list of matches and pulling data on matches

  for matchid in LastFiftyMatches:
    #print("matchid=", matchid)
    #print("match data=",  reqMatchData(matchid))
    
    matchinfo=reqMatchData(matchid)
    num_participants=len(matchinfo['metadata']['participants'])
    print("num_participants=", num_participants)

    i=0
    blueAssists=0
    redAssists=0

    blueGold=0
    redGold=0

    blueKills=0
    redKills=0

    while i<num_participants/2: # because not all games has the same number of participants - first half are blue team
      blueAssists+=matchinfo['info']['participants'][i]['assists'] # total number of assists by blue team
      blueGold+=matchinfo['info']['participants'][i]['goldEarned'] # total number of gold
      blueKills+=matchinfo['info']['participants'][i]['kills'] # total number of kills
      i+=1

    while i>=num_participants/2 and i<num_participants:
      redAssists+=matchinfo['info']['participants'][i]['assists']
      redGold+=matchinfo['info']['participants'][i]['goldEarned']
      redKills+=matchinfo['info']['participants'][i]['kills']
      i+=1

    if matchinfo['info']['participants'][0]['win'] == True: # if first player wins, then blue team won that match
      outcome=1 # 1 means blue team win
    else:
      outcome=0 # 0 means red team win

    gamelength=matchinfo['info']['gameDuration'] # finding length of game

    print("Total blueKills in Match", matchnum, "=", blueKills)
    print("Total redKills in Match", matchnum, "=", redKills)
      
    print("Total blueAssists in Match", matchnum, "=", blueAssists)
    print("Total redAssists in Match", matchnum, "=", redAssists)


    print("Total blueGold in Match", matchnum, "=", blueGold)
    print("Total redGold in Match", matchnum, "=", redGold)

    print("Game Duration in Match", matchnum, "=",   gamelength)
    print("Outcome in Match", matchnum, "=",   outcome)

    data=[matchnum, blueKills, redKills, blueAssists, redAssists, blueGold, redGold, gamelength, outcome] # indicating what to write as data
    # print("data=", data)

    matchnum+=1 # iterating through next match
    writer.writerow(data) # writing data into CSV

    time.sleep(1)





