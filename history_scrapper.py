import csv
from bs4 import BeautifulSoup
from urllib2 import urlopen
import difflib

year = 2016
week = 11
pos = ""

while week < 18:
    player_info = []
    all_players = {}

    #Scrape Rotoguru
    #url = "http://rotoguru1.com/cgi-bin/fyday.pl?week=" + str(week) + "&game=fd"
    url = "http://rotoguru1.com/cgi-bin/fyday.pl?week=" + str(week) + "&year=2016&game=fd"
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    tables = soup.findAll("tr")

    d_indicator = ""; qb_indicator = ""; rb_indicator = ""; wr_indicator = ""; te_indicator = ""; k_indicator = ""

    for table in tables:
        line = table.get_text(" ")
        player = line.split(" ")

        player_info = [year,str(week),0,0,0,0,0,"na",0]
    
        #set up indicator variable to treat the Defenses name differently
        if player[0] == "Defenses":
            d_indicator = "Yes"
        if player[0] == "Quarterbacks":
            qb_indicator = "Yes"
        if player[0] == "Running":
            rb_indicator = "Yes"
            qb_indicator = ""
        if player[0] == "Wide":
            wr_indicator = "Yes"
            rb_indicator = ""
        if player[0] == "Tight":
            te_indicator = "Yes"
            wr_indicator = ""
        if player[0] == "Kickers":
            k_indicator = "Yes"
            te_indicator = ""
    

        tm = ""
        home = ""
        opp = ""


        #filter for player lines that are not defenses
        if "$" in player[len(player) - 1] and not d_indicator:
        
            if qb_indicator:
                pos = "QB"
            if rb_indicator:
                pos = "RB"
            if wr_indicator:
                pos = "WR"
            if te_indicator:
                pos = "TE"
            if k_indicator:
                pos = "K"
        
            #filter for players with only two items for first and last name
            if player[2][0].islower():
                player_name = player[1].encode('ascii','ignore') + " " + \
                player[0][:len(player[0])-1].encode('ascii','ignore')
                
                tm = player[2]

                if "v" in player[3]:
                    home = 1
                elif "@" in player[3]:
                    home = 0
                
                opp = player[4]

            #filter for players who have three items for name - e.g. Ted Ginn Jr.
            else:
                player_name = player[2].encode('ascii','ignore') + " " + \
                player[0].encode('ascii','ignore') + " " + \
                player[1][:len(player[0])-1].encode('ascii','ignore')
        
                tm = player[3]

                if "v" in player[4]:
                    home = 1
                elif "@" in player[4]:
                    home = 0

                opp = player[5]

            #add position, team, points and salary to player dictionary
            try:
                all_players[player_name] = player_info
                all_players[player_name][2] = pos
                all_players[player_name][3] = tm
                all_players[player_name][4] = player[len(player) - 1].encode('ascii','ignore' )
                all_players[player_name][5] = player[len(player) - 2].encode('ascii','ignore')
                all_players[player_name][7] = home
                all_players[player_name][8] = opp

            #if error, print player
            except (KeyError,IndexError) as error:
                print "roto-guru player not found:", player, player_name, error

        #filter for defenses
        elif "$" in player[len(player) - 1] and d_indicator:
        
            pos = "D"
            
            #one name defenses
            if player[1][0].islower():
                player_name = player[0].encode('ascii','ignore')
                tm = player[1]
                
                if "v" in player[2]:
                    home = 1
                elif "@" in player[2]:
                    home = 0
                
                opp = player[3]

            #two name defenses
            elif player[2][0].islower(): 
                if year == 2016:
                    player_name = player[0].encode('ascii','ignore')
                else:
                    player_name = player[0].encode('ascii','ignore') + " " +  player[1].encode('ascii','ignore')
                
                tm = player[2]
                
                if "v" in player[3]:
                    home = 1
                elif "@" in player[3]:
                    home = 0

                opp = player[4]

            #three name defenses
            elif player[3][0].islower():
                if year == 2016:
                    player_name = player[0].encode('ascii','ignore') + " " + player[1].encode('ascii','ignore')
                else:
                    player_name = player[0].encode('ascii','ignore')  + " " + \
                    player[1].encode('ascii','ignore') + " " + player[2].encode('ascii','ignore')
                tm = player[3]
                
                if "v" in player[4]:
                    home = 1
                elif "@" in player[4]:
                    home = 0
                
                opp = player[5]

            else:
                if year == 2016:
                    player_name = player[0].encode('ascii','ignore') + " " + player[1].encode('ascii','ignore') + \
                    " " + player[2].encode('ascii', 'ignore')
                
                tm = player[4]
                
                if "v" in player[5]:
                    home = 1
                elif "@" in player[5]:
                    home = 0
                
                opp = player[6]

            try:
                all_players[player_name] = player_info
                all_players[player_name][2] = pos
                all_players[player_name][3] = tm
                all_players[player_name][4] = player[len(player) - 1].encode('ascii','ignore' )
                all_players[player_name][5] = player[len(player) - 2].encode('ascii','ignore')
                all_players[player_name][7] = home
                all_players[player_name][8] = opp

            except (KeyError,IndexError) as error:
                print "roto-guru player not found:", player, player_name, erorr



    #Scrape linestar txt file for ownership percentage and add to dictionary
    with open(str(year)+ "_" + str(week) +'.txt', 'r') as player_file:
        reader = csv.reader(player_file, delimiter=",")
        for row in reader:
            if len(row) > 4 and row[4].split(":")[1][1:4]:
                player_name = row[1].split(":")[1]
                
                #fix issue with non-matching of Arizona Cardinals with Arizona
                if "Arizona" in player_name:
                    player_name = "Arizona C"
                if "Miami" in player_name:
                    player_name = "Miami D"

                player_name = difflib.get_close_matches(player_name[1:len(player_name)-1], \
                        [keys for keys in all_players.keys()], n=1)
                ownership_percent = row[2].split(":")[1]

                try:
                    all_players[player_name[0]][6] = ownership_percent
        
                except (KeyError,IndexError) as error:
                    print "linestar player not found:", row, player_name, row[1].split(":")[1][1:len(player_name)-1], year, week, error

    #Write results to file
    with open('players_database' + str(year) + "_" + str(week) + '.csv', 'w') as players_output:
        writer = csv.writer(players_output, delimiter=",")
        #writer.writerow(["player", "year", "week", "position", "team", "salary", "pts", "ownership", "home", "opponent"])
        for key,values in all_players.iteritems():
            if len(values) > 4:
                writer.writerow([key,values[0],values[1],values[2],values[3], values[4], values[5], values[6], values[7], values[8]])

    week += 1
