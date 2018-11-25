# Baseball-Reference-Extracts
Different python codes that help with pulling information of MLB baseball games from Baseball Reference
# get_all_season_innings.py
Pulling every inning of every game from the input season from https://www.baseball-reference.com. 
    
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

# JSON Files (baseball_season_XXXX_full.json)
If you do not want to manually web scrape the values from the get_all_season_innings.py script, I have pulled the same information for the 2015-2018 seasons. They have all of the same information as the output of the get_all_season_innings.py script, with the overall heading key being the season year. They are JSON files, so the easiest way to pull in the information is with the following code:
    
    import json
    seasons = [2015,2016,2017,2018]

    for season in seasons:
        # For each season, load in the web scraped data json file
        with open('baseball_season_{}_full.json'.format(season)) as f:
            globals()['season_{}'.format(season)] = json.load(f)
