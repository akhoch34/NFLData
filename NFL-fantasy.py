from BeautifulSoup import BeautifulSoup
import urllib
import pandas as pd
import numpy as np
import datetime

siteParams = {
    'Position': 'RB%2CWR%2CTE',
    'Year': 2010,
    'Week': 'all',
    'Rules': '1'
}

playersDf = pd.DataFrame()


def parseSoupIntoDf(rawHtml, year):
    global playersDf
    table = rawHtml.findAll('table')[0].findAll('tr')
    del table[0]
    del table[0]        # remove first two header rows in table
    for row in table:
        col = row.findAll('td')
        nameTeam = col[0].findAll('span')
        nameTeam = str(nameTeam[0].text).strip()
        name, team = nameTeam.split(',')
        team = team[1:]
        fantasyPoints = float(str(col[2].text).strip())   #TO DO: manually calculate fantasy points based on Yahoo Scoring System
        rushYards = int(str(col[10].text).strip().replace(',', ''))
        rushTds = int(str(col[11].text).strip())
        receivingYards = int(str(col[14].text).strip().replace(',', ''))
        receivingTds = int(str(col[15].text).strip())
        fumbles = int(str(col[17].text).strip())
        yards = rushYards + receivingYards
        tds = rushTds + receivingTds


        playersDf = playersDf.append({
            'Name': name,
            'Year': year,
            'Team': team,
            'Points': fantasyPoints,
            'Yards': yards,
            'TDs': tds,
            'Fumbles': fumbles
        }, ignore_index=True)


now = datetime.datetime.now()


while siteParams['Year'] < now.year:
    site = urllib.urlopen(
        'http://www.footballdb.com/fantasy-football/index.html?pos=' + siteParams['Position'] + '&yr=' + str(
            siteParams['Year']) + '&wk=' + siteParams['Week'] + '&rules=' + siteParams['Rules']).read()
    soup = BeautifulSoup(site)
    parseSoupIntoDf(soup, str(siteParams['Year']))
    siteParams['Year'] += 1

print playersDf



