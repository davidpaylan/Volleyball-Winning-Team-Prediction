#Import dependencies
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd
#The homepage of the url we will be scraping from:
url = "https://www.plusliga.pl/"
pd.set_option('display.max_columns', None)
import csv
# The file we will be writing to
csv_file = 'PlusLiga.csv'

# All the features we will be collecting from the website
header_row=['Team 1', 'Team 2', 'Score', 'Time', 'Points1', 'Points2',
            'ServeEff1', 'ServeEff2', 'PosPercent1','PosPercent2',
            'KillPercent1', 'KillPercent2', 'EffPercent1', 'EffPercent2']
# This is the website with the 2023 games
homepage_response = requests.get("https://www.plusliga.pl/games/tour/"
                                "2022.html?memo=%7B%22games%22%3A%7B%2"
                                "2tab%22%3A%22table-big%22%7D%7D")
homepage_soup = BeautifulSoup(homepage_response.text, "html.parser")
# The aforementioned website has a bunch of tables each with scores and other
# info. Matchtable will store all of these tables and we will iterate through
# the desired matchtables
matchtable = homepage_soup.findAll('div',
 {'class': 'row text-center gridtable games'})
# Dflist will be used later to store each new row of features
# we get from each iteration, each matchtable
dflist = []

# These are the tables we want to look at
for index in range(60, 339):
    current_table = matchtable[index]
    # I used a simple if statement for specific indices because these indices
    # had different properties from the rest of them, and since there were only
    # two such instances, it was simplest to do an if else checking for these
    if index == 90:
        subinfo = current_table.find('div', {'class':'col-xs-4 col-sm-3 tablecell gold-left'})
    else:
        subinfo = current_table.findAll('div', {'class': 'col-xs-4 col-sm-3 tablecell'})[0]
    a_element = subinfo.find("a")
    # Getting the team 1 name, team 2 name, and score and time data
    # Team 1 being the team on the left, Team 2 being the team on the right
    team1 = a_element.text
    if index == 84:
        subinfo2 = current_table.find('div', {'class': 'col-xs-4 col-sm-3 tablecell gold-right'})
    elif index == 90:
        subinfo2 = current_table.findAll('div', {'class': 'col-xs-4 col-sm-3 tablecell'})[0]
    else:
        subinfo2 = current_table.findAll('div', {'class': 'col-xs-4 col-sm-3 tablecell'})[1]
    b_element = subinfo2.find("a")
    team2 = b_element.text
    subinfo3 = current_table.find('div', {'class': 'col-xs-4 col-sm-2 tablecell'})
    score = subinfo3.find('div',{'class':'gameresult clickable'})
    score = score.text
    time = subinfo3.find('div',{'class':'date khanded'})
    time = time.text
    # In each matchtable, each iteration, there is a link for more info on a specific game.
    # Here we find the link element and join it with the homepage url to call requests.get and parse
    link_element = current_table.find('a',{'class':'btn btn-default btm-margins'})
    linkurl = link_element['href']
    full_link_url = urljoin(url, linkurl)
    linked_page_response = requests.get(full_link_url)
    linked_page_soup = BeautifulSoup(linked_page_response.content,'html.parser')
    # Here is table1 and table2, the data for Team 1 and Team 2, respectively.
    table1 = linked_page_soup.findAll('table',{'class':'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive'})[0]
    table2 = linked_page_soup.findAll('table',{'class':'rs-standings-table stats-table table table-bordered table-hover table-condensed table-striped responsive double-responsive'})[1]
    if index == 84 or index == 90:
        Points1 = table1.findAll('tr')[-1].findAll('td')[7].text  # Total pts across all the sets that team 1 got
        Points2 = table2.findAll('tr')[-1].findAll('td')[7].text

        ServeEff1 = table1.findAll('tr')[-1].findAll('td')[13].text # Serve efficiency % of team 1
        ServeEff2 = table2.findAll('tr')[-1].findAll('td')[13].text

        PosPercent1 = table1.findAll('tr')[-1].findAll('td')[16].text  # Reception Positional % of Team 1
        PosPercent2 = table2.findAll('tr')[-1].findAll('td')[16].text
        KillPercent1 = table1.findAll('tr')[-1].findAll('td')[22].text  # Kill % for hitting
        KillPercent2 = table2.findAll('tr')[-1].findAll('td')[22].text
        EffPercent1 = table1.findAll('tr')[-1].findAll('td')[23].text  # Efficiency % for hitting
        EffPercent2 = table2.findAll('tr')[-1].findAll('td')[23].text
    else:
        Points1 = table1.findAll('tr')[-1].findAll('td')[6].text # total pts across all the sets that team 1 got against team 2
        Points2 = table2.findAll('tr')[-1].findAll('td')[6].text

        ServeEff1 = table1.findAll('tr')[-1].findAll('td')[12].text
        ServeEff2 = table2.findAll('tr')[-1].findAll('td')[12].text

        PosPercent1 = table1.findAll('tr')[-1].findAll('td')[15].text # for receiving
        PosPercent2 = table2.findAll('tr')[-1].findAll('td')[15].text
        KillPercent1 = table1.findAll('tr')[-1].findAll('td')[21].text # for hitting
        KillPercent2 = table2.findAll('tr')[-1].findAll('td')[21].text
        EffPercent1 = table1.findAll('tr')[-1].findAll('td')[22].text # for hitting
        EffPercent2 = table2.findAll('tr')[-1].findAll('td')[22].text
    # Make a list new_row and add it into our dflist
    new_row = [team1, team2, score, time,
               Points1, Points2, ServeEff1, ServeEff2, PosPercent1, PosPercent2, KillPercent1, KillPercent2, EffPercent1, EffPercent2]

    dflist.append(new_row)
# Bring all of this data into a dataframe with the columns labeled below
finaldf = pd.DataFrame(dflist, columns = ['Team1','Team2','Score','Time', 'Points1', 'Points2', 'ServeEff1', 'ServeEff2', 'PosPercent1','PosPercent2',
            'KillPercent1', 'KillPercent2', 'EffPercent1', 'EffPercent2'])
# Making the score easier to read
finaldf['Score'] = finaldf['Score'].str.replace(r'\n','',regex=True)
#Separating the score from one column into two columns one for each team
splitscores = finaldf['Score'].str.split(':',expand=True)
finaldf['Score1'] = splitscores[0]
finaldf['Score2'] = splitscores[1]
finaldf.drop(columns=['Score'], inplace=True)
#Export it to a csv
finaldf.to_csv("PlusLiga.csv", index=False)

