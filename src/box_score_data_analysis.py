import json
import pandas as pd
from matplotlib import pyplot as plt
from src.BoxScore import BoxScore
import datetime
import time
import statistics
start_time = datetime.datetime.now()

with open('data/box_score_data_small.json', 'r') as f:
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
aggregation_function = {'blown_leads': 'sum'}
blown_leads_total_data = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)
blown_leads_total_data = blown_leads_total_data.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])
blown_leads_total_data.plot.bar()
plt.show()

# number of total blown leads per team per season
seasons = box_score_data_frame['season'].unique()
blown_leads_all_seasons = pd.DataFrame()

for season in seasons:
    blown_leads_single_season = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()
    blown_leads_single_season['team_abbrv'] = blown_leads_single_season['team_abbrv'].apply(lambda x: f'{x}_{season}')
    aggregation_function = {'blown_leads': 'sum'}
    blown_leads_single_season = blown_leads_single_season.groupby('team_abbrv').aggregate(aggregation_function)
    blown_leads_all_seasons = blown_leads_all_seasons.append(blown_leads_single_season)
blown_leads_all_seasons = blown_leads_all_seasons.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])
blown_leads_all_seasons.plot.bar()
plt.show()

# range of blown leads for the league (with team id)
max_blown_leads_total = box_score_data_frame['blown_leads'].max()
max_blown_leads_total_data_frame = box_score_data_frame.where(box_score_data_frame['blown_leads'] == max_blown_leads_total).dropna()
min_blown_leads_total = box_score_data_frame['blown_leads'].min()
min_blown_leads_total_data_frame = box_score_data_frame.where(box_score_data_frame['blown_leads'] == min_blown_leads_total).dropna()

# range of blown leads for the league (with team id) per season (# don't need to graph, just useful as stats)
seasons = box_score_data_frame['season'].unique()
max_blown_leads_all_seasons = pd.DataFrame()
for season in seasons:
    season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)
    max_blown_leads_season = season_data_frame['blown_leads'].max()
    max_blown_leads_data = season_data_frame.where(season_data_frame['blown_leads'] == max_blown_leads_season).dropna()
    max_blown_leads_all_seasons = max_blown_leads_all_seasons.append(max_blown_leads_data)

# mean, median, mode, range of blown leads for the league
blown_leads_all_seasons_dict = {}
blown_leads_all_seasons_dict['mean'] = blown_leads_total_data['blown_leads'].mean()
blown_leads_all_seasons_dict['mode'] = blown_leads_total_data['blown_leads'].mode()[0]
blown_leads_all_seasons_dict['median'] = blown_leads_total_data['blown_leads'].median()
blown_leads_total_data.plot.box()
plt.show()

# mean, median, mode, range of blown leads for the league per season
seasons = box_score_data_frame['season'].unique()
teams = box_score_data_frame['team_abbrv'].unique()
blown_leads_per_season_box_plot_data = pd.DataFrame(index=teams)
blown_leads_per_season_dict = {}

for season in seasons:
    # dataframe stuff
    blown_leads_single_season_box_plot_data = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()
    aggregation_function = {'blown_leads': 'sum'}
    blown_leads_single_season_box_plot_data = blown_leads_single_season_box_plot_data.groupby('team_abbrv').aggregate(aggregation_function)
    blown_leads_single_season_box_plot_data = blown_leads_single_season_box_plot_data.rename(columns={'blown_leads': f'blown_leads_{season}'})
    blown_leads_per_season_box_plot_data = blown_leads_per_season_box_plot_data.merge(blown_leads_single_season_box_plot_data, left_index=True, right_index=True)

    # stats dict stuff
    season_stats_dict = {}
    mean_blown_leads = blown_leads_single_season['blown_leads'].mean()
    mode_blown_leads = blown_leads_single_season['blown_leads'].mode()[0]
    median_blown_leads = blown_leads_single_season['blown_leads'].median()
    season_stats_dict['mean'] = mean_blown_leads
    season_stats_dict['mode'] = mode_blown_leads
    season_stats_dict['median'] = median_blown_leads
    blown_leads_per_season_dict[season] = season_stats_dict

blown_leads_per_season_box_plot_data.plot.box()
plt.show()

# mean, median, mode, range of of blown leads for STL
stl_blown_leads_stats_dict = {}
stl_blown_leads = blown_leads_per_season_box_plot_data.loc['STL']
stl_blown_leads.plot.box()
plt.show()

blown_leads_max = stl_blown_leads.max()
blown_leads_max_season = stl_blown_leads.idxmax()
stl_blown_leads_stats_dict['maximum'] = {blown_leads_max_season: blown_leads_max}

blown_leads_min = stl_blown_leads.min()
blown_leads_min_season = stl_blown_leads.idxmin()

stl_blown_leads_stats_dict['minimun'] = {blown_leads_min_season: blown_leads_min}
stl_blown_leads_stats_dict['mean'] = stl_blown_leads.mean()
stl_blown_leads_stats_dict['mode'] = stl_blown_leads.mode()
stl_blown_leads_stats_dict['median'] = stl_blown_leads.median()

# number of times STL blew at least 1 lead and lost
seasons = box_score_data_frame['season'].unique()
stl_blown_leads_all_seasons_data_dict = {}
stl_blown_leads_data = box_score_data_frame.where(
    (box_score_data_frame['team_abbrv'] == 'STL') &
    (box_score_data_frame['blown_leads'] > 0) &
    (box_score_data_frame['result'] == 0)
).dropna()

stl_blown_leads_lead_losses_total = len(stl_blown_leads_data.index)
stl_blown_leads_lead_losses_per_season = {}
for season in seasons:
    stl_blown_leads_single_season_data = stl_blown_leads_data.where(stl_blown_leads_data['season'] == season).dropna()
    stl_blown_leads_single_season = len(stl_blown_leads_single_season_data.index)
    stl_blown_leads_lead_losses_per_season[season] = stl_blown_leads_single_season

stl_blown_leads_lead_average_per_season = list(stl_blown_leads_lead_losses_per_season.values())
stl_blown_leads_lead_average_per_season = statistics.mean(stl_blown_leads_lead_average_per_season)

stl_blown_leads_all_seasons_data_dict['total'] = stl_blown_leads_lead_losses_total
stl_blown_leads_all_seasons_data_dict['average'] = stl_blown_leads_lead_average_per_season
stl_blown_leads_all_seasons_data_dict['seasons'] = stl_blown_leads_lead_losses_per_season
