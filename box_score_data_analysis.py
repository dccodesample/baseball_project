import json
import pandas as pd
from matplotlib import pyplot as plt
from BoxScore import BoxScore
import datetime

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
teams = list(box_score_data_frame['team_abbrv'].unique())
blown_leads_total_data = {}
for team in teams:
    blown_leads_for_team = int(box_score_data_frame.where(box_score_data_frame['team_abbrv'] == team)['blown_leads'].sum())
    blown_leads_total_data[team] = blown_leads_for_team

blown_leads_total_data_sorted = sorted([(value, key) for (key, value) in blown_leads_total_data.items()], reverse=True)
y, x = zip(*blown_leads_total_data_sorted)
print(blown_leads_total_data_sorted)

plt.bar(x, y)
plt.show()

# box_score_data_frame.groupby(['team_abbrv'])['blown_leads'].sum()

# number of total blown leads per team per season
# box_score_data_frame.groupby(['team_abbrv', 'season'])['blown_leads'].sum()

# range of blown leads for the league (with team id)
# max_blown_leads_total = box_score_data_frame['blown_leads'].max()
# max_blown_leads_total_data_frame = box_score_data_frame.where(box_score_data_frame['blown_leads'] == max_blown_leads_total).dropna()
# min_blown_leads_total = box_score_data_frame['blown_leads'].min()
# min_blown_leads_total_data_frame = box_score_data_frame.where(box_score_data_frame['blown_leads'] == min_blown_leads_total).dropna()

# range of blown leads for the league (with team id) per season
# seasons = box_score_data_frame['season'].unique()
# max_blown_leads_per_season = []
# for season in seasons:
#     # max_blown_leads_season = box_score_data_frame.where(box_score_data_frame['season'] == season)['blown_leads'].max()
#     # box_score_data_frame.where((box_score_data_frame['season'] == season) & (box_score_data_frame['blown_leads'] == max_blown_leads_season)).dropna()
#     season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)
#     max_blown_leads_season = season_data_frame['blown_leads'].max()
#     max_blown_leads_data = season_data_frame.where(season_data_frame['blown_leads'] == max_blown_leads_season)



# mean, median, mode of blown leads for the league
# mean, median, mode of blown leads for the league per season
# number of blown leads for STL
# number of blown leads for STL per season
# range of blown leads for STL for the dataset
# number of times STL blew at least 1 lead and lost
