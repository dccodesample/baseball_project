import json
import pandas as pd
from matplotlib import pyplot as plt
from src.BoxScore import BoxScore
import datetime
import time

start_time = datetime.datetime.now()

with open('data/box_score_data.json', 'r') as f:
    box_score_data = json.load(f)

box_score_data_frame = pd.DataFrame()
for team in box_score_data:
    for season in box_score_data[team]:
        for box_score_id in box_score_data[team][season]:
            box_score_raw = box_score_data[team][season][box_score_id]
            box_score = BoxScore(box_score_raw, box_score_id, season, team)

            columns = list(box_score.__dict__.keys())
            values = list(box_score.__dict__.values())
            temp_data_frame = pd.DataFrame([values], columns=columns)
            box_score_data_frame = box_score_data_frame.append(temp_data_frame)


end_time = datetime.datetime.now()
print(f'Total Time: {end_time - start_time}')

# number of total blown leads per team
# aggregation_function = {'blown_leads': 'sum'}
# blown_leads_total_data = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)
# blown_leads_total_data = blown_leads_total_data.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])
# blown_leads_total_data.plot.bar()
# plt.show()

# number of total blown leads per team per season
# seasons = box_score_data_frame['season'].unique()
# blown_leads_all_seasons = pd.DataFrame()

# for season in seasons:
#     blown_leads_single_season = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()
#     blown_leads_single_season['team_abbrv'] = blown_leads_single_season['team_abbrv'].apply(lambda x: f'{x}_{season}')
#     aggregation_function = {'blown_leads': 'sum'}
#     blown_leads_single_season = blown_leads_single_season.groupby('team_abbrv').aggregate(aggregation_function)
#     blown_leads_all_seasons = blown_leads_all_seasons.append(blown_leads_single_season)
# blown_leads_all_seasons = blown_leads_all_seasons.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])
# blown_leads_all_seasons.plot.bar()
# plt.show()

# range of blown leads for the league (with team id)
# don't need to graph, just useful as stats
# max_blown_leads_total = box_score_data_frame['blown_leads'].max()
# max_blown_leads_total_data_frame = box_score_data_frame.where(box_score_data_frame['blown_leads'] == max_blown_leads_total).dropna()
# min_blown_leads_total = box_score_data_frame['blown_leads'].min()
# min_blown_leads_total_data_frame = box_score_data_frame.where(box_score_data_frame['blown_leads'] == min_blown_leads_total).dropna()


# range of blown leads for the league (with team id) per season
# don't need to graph, just useful as stats
# seasons = box_score_data_frame['season'].unique()
# max_blown_leads_per_season = []
# for season in seasons:
#     # max_blown_leads_season = box_score_data_frame.where(box_score_data_frame['season'] == season)['blown_leads'].max()
#     # box_score_data_frame.where((box_score_data_frame['season'] == season) & (box_score_data_frame['blown_leads'] == max_blown_leads_season)).dropna()
#     season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)
#     max_blown_leads_season = season_data_frame['blown_leads'].max()
#     max_blown_leads_data = season_data_frame.where(season_data_frame['blown_leads'] == max_blown_leads_season)



# mean, median, mode, range of blown leads for the league
#   box and whiskers plot (one plot for all teams obvi)
# mean, median, mode, range of blown leads for the league per season
#   box and whiskers plot (one plot for all teams for a single year obvi)

# mean, median, mode, range of of blown leads for STL
# box and whiskers plot
# number of blown leads for STL per season
# range of blown leads for STL for the dataset
# just calculate, no plot
# number of times STL blew at least 1 lead and lost
# total, average per season
