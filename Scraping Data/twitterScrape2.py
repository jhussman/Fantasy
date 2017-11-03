#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 17:05:21 2017

@author: harsheelsoin
"""

import csv
import unicodedata
from selenium import webdriver
#from bs4 import BeautifulSoup

allNames=[]
startDates=[]
endDates=[]

with open('/Users/harsheelsoin/Downloads/Projects in Data Science/Semester Project/COMS6998_Proj-master/playerQueries.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        name, startDate, endDate = row[0], row[1], row[2]
        allNames.append(name)
        startDates.append(startDate)
        endDates.append(endDate)

urlPart1 = 'https://twitter.com/search?l=en&q='
urlPart3 = 'since%3A'
urlPart4 = '%20until%3A'
urlPart5 = '&src=typd&lang=en'

allURLs = []

for i in range(0,len(allNames)):
    nameParts = allNames[i].split(" ")
    urlPart2 = ""
    for part in nameParts:
        part=part.lower()
        part=part+"%20"
        urlPart2+=part
    url = urlPart1+urlPart2+urlPart3+startDates[i]+urlPart4+endDates[i]+urlPart5
    allURLs.append(url)

#print allURLs[0]
browser = webdriver.Chrome()
tweetNameCounts=[]
allX=[]

for i in range(5000,6043):
    browser.get(allURLs[i])
    pagewith = browser.page_source
    pagewith2 = unicodedata.normalize('NFKD', pagewith).encode('ascii','ignore')
    pagewith2 = pagewith2.lower()
    x=[]
    x.append(pagewith2.count(allNames[i].lower()))
    nameComps = allNames[i].split(" ")
    for comp in nameComps:
        x.append(pagewith2.count(comp.lower()))
    allX.append(x)
    y=max(x)
    tweetNameCounts.append(y)

print allX
print tweetNameCounts

with open('/Users/harsheelsoin/Downloads/Projects in Data Science/Semester Project/COMS6998_Proj-master/players_database.csv', 'rb') as fin:
    with open('/Users/harsheelsoin/Downloads/Projects in Data Science/Semester Project/COMS6998_Proj-master/players_database_tweets.csv', 'wb') as fout:
        writer1 = csv.writer(fout, delimiter=',')
        reader1 = csv.reader(fin, delimiter=',')
        allFinalRows=[]
        row=next(reader1)
        row.append("tweetCounts")
        allFinalRows.append(row)
        
        for i in range(0,len(tweetNameCounts)):
            row = next(reader1)
            row.append(tweetNameCounts[i])
            allFinalRows.append(row)
        
        writer1.writerows(allFinalRows)

with open('/Users/harsheelsoin/Downloads/Projects in Data Science/Semester Project/COMS6998_Proj-master/playerQueries_tweets.csv', 'wb') as fout2:
    writer2 = csv.writer(fout2, delimiter=',')
    allFinalRows2=[]
    row = ["player", "queryStartDate", "queryEndDate", "allQueryTweetCounts", "maxTweetCounts"]
    allFinalRows2.append(row)
    for i in range(0,len(allNames)):
        row = [allNames[i], startDates[i], endDates[i], allX[i], tweetNameCounts[i]]
        allFinalRows2.append(row)
    writer2.writerows(allFinalRows2)