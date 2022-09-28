import requests
import time

#me, dd, jk, gl, doubi, pl, shuhong
players = {"351777742":"<@551762924935577610>","1072053692":"<@686915314574688379>",
           "289492680":"<@527518736295395348>","344137792":"<@559762654084857876>",
           "322201019":"<@683677328815161485>","1131642329":"<@523365677189562378>",
           "1191609180":"<@368800880511942667>"}

def processed_match(match_id):
    try:
        with open("matches.txt","r") as matchesFile:
            matches = matchesFile.read()
        if str(match_id) in matches:
            return True
        return False
    except:
        return False
def record_processed_match(match_id):
    if not processed_match(match_id):
        with open("matches.txt","a+") as matchesFile:
            matchesFile.write(str(match_id)+"\n")
    
def request_parse_match(match_id):
    request_parse_url = f"https://api.opendota.com/api/request/{match_id}"
    response = requests.post(request_parse_url)
    if response.status_code == 200:
        return True
    return False
def parse_recent_matches(player_id):
    try:
        response = requests.get(f"https://api.opendota.com/api/players/{player_id}/recentMatches").json()
        for match in response[:10]:
            match_id = match["match_id"]
            match_parsed = match["version"]

            win = False
            player_slot = match["player_slot"]
            radiant_win = match["radiant_win"]
            if player_slot >= 128:
                if not radiant_win:
                    win = True
            else:
                if radiant_win:
                    win = True
            if win:
                winText = "Win"
            else:
                winText = "Lose"
                
            if not processed_match(match_id):
                if not match_parsed:
                    request_succeed = request_parse_match(match_id)
                    if request_succeed:
                        #Send webhook to inform
                        webhook = "https://discord.com/api/webhooks/1014258748207943701/PIv1JmrCkp-sB5cEdm_EmzO-rwxEDXsIhdABpjbwxiMTYegHlB8fLGTk-0yZlp113aLo"
                        jsonObj = {"content":players[player_id]+", your game is parsed and you can check it on <https://www.opendota.com/matches/"+str(match_id)+"> - "+winText}
                        requests.post(webhook,json=jsonObj)
                        
                        print("Request succeed for player",player_id," - match",match_id)
                        record_processed_match(match_id)
                    else:
                        print("Request failed for player",player_id," - match",match_id)
    except Exception as e:
        print("Error processing for player "+str(e))


while True:
    for playerid in players:
        parse_recent_matches(playerid)
    time.sleep(1200)
