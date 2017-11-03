import csv
from bs4 import BeautifulSoup
from urllib2 import urlopen
import difflib


'''
Open official FanDuel players list for given week and save relevant variables to dictionary
'''
player_info = []
all_players = {}
with open('FanDuel-NFL-2017-10-26-21634-players-list.csv', 'r') as player_file:
    reader = csv.reader(player_file, delimiter=",")
    next(reader,None)
    for row in reader:
        player_info = []
        ids = row[0].split('-')
        player_info.extend((ids[1],"7",row[1],row[9], "0", "0", "0"))
        all_players[row[3]] = player_info


'''
Scrape data from rotoguru and add it to FanDuel official palyer dictionary
'''
url = "http://rotoguru1.com/cgi-bin/fyday.pl?week=7&game=fd"
page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
tables = soup.findAll("tr")

indicator = ""
bye_week = ["ari","gnb","jac","lar","ten","nyg"]
for table in tables:
    line = table.get_text(" ")
    player = line.split(" ")

    #set up indicator variable to treat the Defenses name differently
    if player[0] == "Defenses":
        indicator = "Yes"

    #filter for player lines that are not defenses
    if "$" in player[len(player) - 1] and not indicator and player[2] not in bye_week and player[3] not in bye_week:
        
        #filter for players with only two items for first and last name
        if player[2][0].islower():
            player_name = difflib.get_close_matches(player[1].encode('ascii','ignore') + " " + \
            player[0][:len(player[0])-1].encode('ascii','ignore'), [keys for keys in all_players.keys()], n=1)
        
        #filter for players who have three items for name - e.g. Ted Ginn Jr.
        else:
            player_name = difflib.get_close_matches(player[2].encode('ascii','ignore') + " " + \
            player[0].encode('ascii','ignore') + " " + \
            player[1][:len(player[0])-1].encode('ascii','ignore'), [keys for keys in all_players.keys()], n=1)

        #add points and salary to player dictionary
        try:
            all_players[player_name[0]][4] = player[len(player) - 1].encode('ascii','ignore' )
            all_players[player_name[0]][5] = player[len(player) - 2].encode('ascii','ignore')
        
        #if player not found, print player
        except (KeyError,IndexError) as error:
            print "roto-guru player not found:", player, player_name, error
    
    #filter for defenses
    elif "$" in player[len(player) - 1] and indicator and player[1] not in bye_week and player[2] not in bye_week and player[3] not in bye_week:
        #one name defenses
        if player[1][0].islower():
            #difflib doesn't match Miami - fixed this
            if player[0] == "Miami":
                player[0] = "Miami D"
            player_name = difflib.get_close_matches(player[0].encode('ascii','ignore'), [keys for keys in all_players.keys()], n=1)
       
            try:
                all_players[player_name[0]][4] = player[len(player) - 1].encode('ascii','ignore')
                all_players[player_name[0]][5] = player[len(player) - 2].encode('ascii','ignore')

            except (KeyError,IndexError) as error:
                print "roto-guru player not found:", player, player_name, error
           
        #two name defenses
        elif player[2][0].islower(): 
            player_name = difflib.get_close_matches(player[0].encode('ascii','ignore') + " " +  player[1].encode('ascii','ignore'), [keys for keys in all_players.keys()], n=1)
        
            try:
                all_players[player_name[0]][4] = player[len(player) - 1].encode('ascii','ignore')
                all_players[player_name[0]][5] = player[len(player) - 2].encode('ascii','ignore')

            except (KeyError,IndexError) as error:
                print "roto-guru player not found:", player, player_name, error
        
        #three name defenses
        else:
            player_name = difflib.get_close_matches(player[0].encode('ascii','ignore')  + " " + \
            player[1].encode('ascii','ignore') + " " + player[2].encode('ascii','ignore'), [keys for keys in all_players.keys()], n=1)

            try:
                all_players[player_name[0]][4] = player[len(player) - 1].encode('ascii','ignore')
                all_players[player_name[0]][5] = player[len(player) - 2].encode('ascii','ignore')

            except (KeyError,IndexError) as error:
                print "roto-guru player not found:", player, player_name, erorr


'''
Scrape linestar txt file for ownership percentage and add to dictionary
'''
bye_week = ['ARI','GB','JAC','LAR','TEN','NYG']
with open('ownership_percentage_week7.txt', 'r') as player_file:
    reader = csv.reader(player_file, delimiter=",")
    for row in reader:
        if len(row) > 0 and row[4].split(":")[1][1:4] not in bye_week and row[4].split(":")[1][1:3] not in bye_week:
            player_name = row[1].split(":")[1]
            player_name = difflib.get_close_matches(player_name[1:len(player_name)-1], [keys for keys in all_players.keys()], n=1)
            ownership_percent = row[2].split(":")[1]

            try:
                all_players[player_name[0]][6] = ownership_percent
        
            except (KeyError,IndexError) as error:
                print "linestar player not found:", row, player_name, error

'''
Write results to file
'''
with open('players_database.csv', 'w') as players_output:
    writer = csv.writer(players_output, delimiter=",")
    writer.writerow(["player","player_id","week","position", "team", "salary","pts","ownership"])
    for key,values in all_players.iteritems():
        if len(values) > 4:
            writer.writerow([key,values[0],values[1],values[2],values[3], values[4], values[5], values[6]])
    

