import pandas as pd

the_file = pd.read_csv('Downloads/FanDuel-NFL-2017-10-26-21634-players-list.csv')
the_defense = the_file[the_file.Position == 'D']
the_file = the_file.drop(['Played','Team','Id','First Name','Last Name','Injury Indicator','Injury Details','Unnamed: 13','Unnamed: 14'], axis = 1)
the_file['Home'] = 0
for i in range(len(the_file.Opponent)):
    #stripped = the_file.Game[i].split("@")
    if the_file.Game[i].split("@")[0] == the_file.Opponent[i]:
        the_file.Home[i] = 1
the_file.insert(4, 'Defense', the_file['Opponent'].map(the_defense.set_index('Team')['FPPG']))
the_file = the_file.drop(['Opponent','Game'], axis = 1)
the_file = the_file.rename(columns= {'Defense':'Opponent'})
dummy = pd.get_dummies(the_file['Position'])
the_file = pd.concat([the_file,dummy], axis = 1)
the_file.to_csv('fanduel_current.csv', sep = ',')
