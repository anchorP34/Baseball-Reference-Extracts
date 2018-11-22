import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

def get_all_season_innings_results(season, end_date):
    """
    Description: 
        Pulling every inning of every game from the input season from https://www.baseball-reference.com
    
    INPUT: 
        Season (int) - The season of the MLB year you would like to pull
        end_date (string) - Date of the last game that you would like to pull before
                       Example: If the playoffs in the 2017 season start  October 3, 2017, you want that 
                       to be the stop date. So, for end_date, you would put '20171003' as the stop date.
    
    OUTPUT: 
        all_seasons_dict (dictionary) - Shows the following information about the season for each team
            TotalWins - Total Wins
            TotalLosses - Total Losses
            HomeWins - Number of wins that occured when playing at home
            AwayWins - Number of wins that occured when playing on the road
            HomeLosses - Number of losses that occured when playing at home
            AwayLosses - Number of losses that occured when playing on the road
            TotalGameOutcomes - Array of W's and L's of each game played throughout the year
            HomeGameOutcomes - Array of W's and L's of each home game played throughout the year
            AwayGameOutcomes - Array of W's and L's of each away game played throughout the year
            TotalOffenseInnings - Arrays of each offensive inning for every game of the season. If X, that meant the
                                    inning wasn't needed in the bottom of the 9th
            HomeOffenseInnings - Arrays of each offensive inning for every home game of the season. If X, that meant the
                                    inning wasn't needed in the bottom of the 9th
            AwayOffenseInnings - Arrays of each offensive inning for every away game of the season. 
            TotalDefenseInnings - Arrays of each defensive inning for every game of the season. If X, that meant the
                                    inning wasn't needed in the bottom of the 9th
            HomeDefenseInnings - Arrays of each defensive inning for every home game of the season. If X, that meant the
                                    inning wasn't needed in the bottom of the 9th
            AwayInnings - Arrays of each defensive inning for every away game of the season. 
  
    """
    all_seasons_dict = {}
    seasons = [season]
    end_date_string = str(end_date) + '0'#'201409300' <- Example End Date for 2007

    for season in seasons:

        all_seasons_dict[season] = {}

        season_request = requests.get('https://www.baseball-reference.com/leagues/MLB/{}-schedule.shtml'.format(season))
        season_soup = BeautifulSoup(season_request.text, 'lxml')



        for elem in season_soup(text=re.compile('Boxscore')):
            game_html = list(elem.parent.attrs.values())[0]
            print('https://www.baseball-reference.com' + game_html)
            
            
            if end_date_string is not None and end_date_string in game_html:
                break
            else:

                game_request = requests.get('https://www.baseball-reference.com' + game_html)
                game_soup = BeautifulSoup(game_request.text, 'lxml')

                away_team = game_soup.find(attrs = {"class":"linescore_wrap"}).find('tbody').find_all('a')[2].string
                home_team = game_soup.find(attrs = {"class":"linescore_wrap"}).find('tbody').find_all('a')[-1].string

                for team in [away_team, home_team]:
                # Add teams to dictionary if they don't exist
                    if team not in all_seasons_dict[season]:
                        all_seasons_dict[season][team] = {
                  'TotalWins' : 0
                , 'TotalLosses' : 0

                , 'HomeWins': 0
                , 'AwayWins': 0

                , 'HomeLosses': 0
                , 'AwayLosses': 0

                , 'TotalGameOutcomes': []
                , 'HomeGameOutcomes': []
                , 'AwayGameOutcomes' : []

                , 'TotalOffenseInnings': []
                , 'HomeOffenseInnings' : []
                , 'AwayOffenseInnings' : []

                , 'TotalDefenseInnings': []
                , 'HomeDefenseInnings' : []
                , 'AwayDefenseInnings' : []
          }


                game_boxscore = []
                for x in game_soup.find(attrs = {"class":"linescore_wrap"}).find('tbody').find_all(attrs = {"class": "center"}):
                    if '<div class="media-item logo loader">' not in str(x):
                        game_boxscore.append(x.text)

                away_box = game_boxscore[: int(len(game_boxscore) / 2)]
                home_box = game_boxscore[int(len(game_boxscore) / 2):] 


                away_innings = away_box[:-3]
                home_innings = home_box[:-3]

                # Put the offensive and defensive innings based on home / away
                all_seasons_dict[season][home_team]['HomeOffenseInnings'].append(home_innings)
                all_seasons_dict[season][home_team]['HomeDefenseInnings'].append(away_innings)

                all_seasons_dict[season][away_team]['AwayOffenseInnings'].append(away_innings)
                all_seasons_dict[season][away_team]['AwayDefenseInnings'].append(home_innings)  

                # Record all of the offense and defense innings for each game
                all_seasons_dict[season][away_team]['TotalOffenseInnings'].append(away_innings)
                all_seasons_dict[season][home_team]['TotalOffenseInnings'].append(home_innings)

                all_seasons_dict[season][away_team]['TotalDefenseInnings'].append(home_innings)
                all_seasons_dict[season][home_team]['TotalDefenseInnings'].append(away_innings)


                away_score = away_box[-3]
                home_score = home_box[-3]


                if int(away_score) > int(home_score): #If the away team wins
                    winning_team = away_team
                    all_seasons_dict[season][away_team]['TotalGameOutcomes'].append('W')
                    all_seasons_dict[season][away_team]['AwayGameOutcomes'].append('W')
                    all_seasons_dict[season][away_team]['TotalWins'] += 1
                    all_seasons_dict[season][away_team]['AwayWins'] += 1


                    losing_team = home_team 
                    all_seasons_dict[season][home_team]['TotalGameOutcomes'].append('L')
                    all_seasons_dict[season][home_team]['HomeGameOutcomes'].append('L')
                    all_seasons_dict[season][home_team]['TotalLosses'] += 1
                    all_seasons_dict[season][home_team]['HomeLosses'] += 1


                else: #If the home team wins
                    winning_team = home_team
                    all_seasons_dict[season][home_team]['TotalGameOutcomes'].append('W')
                    all_seasons_dict[season][home_team]['HomeGameOutcomes'].append('W')
                    all_seasons_dict[season][home_team]['TotalWins'] += 1
                    all_seasons_dict[season][home_team]['HomeWins'] += 1            

                    losing_team = away_team
                    all_seasons_dict[season][away_team]['TotalGameOutcomes'].append('L')
                    all_seasons_dict[season][away_team]['AwayGameOutcomes'].append('L')
                    all_seasons_dict[season][away_team]['TotalLosses'] += 1
                    all_seasons_dict[season][away_team]['AwayLosses'] += 1 

                print('\t Away Team: {} - {}\n'.format(away_team, away_score))
                print('\t Home Team: {} - {}\n'.format(home_team, home_score))
                print('\t Winning Team: {} in {} innings\n'.format(winning_team, len(home_innings)))

                print('\t{}\n'.format(away_innings))
                print('\t{}\n'.format(home_innings))
                
    return all_seasons_dict