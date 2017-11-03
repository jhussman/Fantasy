#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 15:23:24 2017

@author: harsheelsoin
"""
import csv
#import timestring
import datetime

t1_16 = datetime.datetime(2016, 9, 13)
w1_16 = datetime.datetime(2016, 9, 14)
t1_17 = datetime.datetime(2017, 9, 12)
w1_17 = datetime.datetime(2017, 9, 13)
#print t1.year, t1.month, t1.day
#tnew = t1+datetime.timedelta(7)
#tnew=str(tnew)
#tnew = tnew.split(" ")[0]


#z = timestring.Date("September 12, 2017")
#z=str(z)
#z=z.split(" ")[0]
#print z

allNames=[]
queryPeriods=[]

with open('/Users/harsheelsoin/Downloads/Projects in Data Science/Semester Project/COMS6998_Proj-master/players_database.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    reader.next()
    for row in reader:
        string1=row[0]
        allNames.append(string1)
        queryPeriod = (row[1],row[2])
        queryPeriods.append(queryPeriod)

#print allNames
#print queryPeriods

allNamesSplit=[]
for name in allNames:
    nameSplit = name.split(" ")
    allNamesSplit.append(nameSplit)

#for i in range(0,len(allNames)):
#    print allNames[i], allNamesSplit[i]
    
#print len(allNames), len(allNamesSplit)
#print allNames[0], allNamesSplit[0]

startDates=[]
endDates=[]
for query in queryPeriods:
    if query[0]=="2016":
        startDate = t1_16 + datetime.timedelta(7*(int(query[1])-1))
        endDate = w1_16 + datetime.timedelta(7*(int(query[1])-1))
    else:
        startDate = t1_17 + datetime.timedelta(7*(int(query[1])-1))
        endDate = w1_17 + datetime.timedelta(7*(int(query[1])-1))
    startDate = str(startDate)
    startDate = startDate.split(" ")[0]
    startDates.append(startDate)
    endDate = str(endDate)
    endDate = endDate.split(" ")[0]
    endDates.append(endDate)

#for i in range(0,len(startDates)):
#    print startDates[i], endDates[i]
#print len(startDates), len(endDates)

with open('/Users/harsheelsoin/Downloads/Projects in Data Science/Semester Project/COMS6998_Proj-master/playerQueries.csv', 'wb') as csvfile:
    queryWriter = csv.writer(csvfile, delimiter=',')
    for i in range(0,len(allNames)):
        row = [allNames[i],startDates[i],endDates[i]]
        queryWriter.writerow(row)