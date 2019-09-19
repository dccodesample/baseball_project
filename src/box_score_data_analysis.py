import json
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams["font.family"] = "Verdana"
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

# number of total blown leads per team
seasons = box_score_data_frame['season'].unique()
aggregation_function = {'blown_leads': 'sum'}

blown_leads_total_data = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)
blown_leads_total_data = blown_leads_total_data.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])


blown_leads_total_data_plot = blown_leads_total_data.plot(kind='bar')
y_ticks = [tick for tick in range((blown_leads_total_data['blown_leads'].max()) + 1)]
blown_leads_total_data_plot.spines['right'].set_visible(False)
blown_leads_total_data_plot.spines['top'].set_visible(False)
blown_leads_total_data_plot.spines['left'].set_edgecolor('0.5')
blown_leads_total_data_plot.spines['left'].set_linewidth(1)
blown_leads_total_data_plot.spines['bottom'].set_edgecolor('0.5')
blown_leads_total_data_plot.spines['bottom'].set_linewidth(1)
plt.title(f'Total Blown Leads: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
plt.xlabel('Teams', labelpad=10, fontsize=12)
plt.ylabel('Blown\nLeads', rotation=0, labelpad=40, fontsize=12)
plt.yticks(y_ticks, fontsize=8)
plt.xticks(fontsize=8)
plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
plt.subplots_adjust(right=0.5)
plt.tight_layout()
plt.savefig('results/blown_leads_total_data_bar_chart.png')



# TODOTODOTODO
# number of total blown leads per team per season
seasons = box_score_data_frame['season'].unique()
blown_leads_all_seasons_data = pd.DataFrame()

for season in seasons:
    blown_leads_single_season = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()
    blown_leads_single_season['team_abbrv'] = blown_leads_single_season['team_abbrv'].apply(lambda x: f'{x}_{season}')
    aggregation_function = {'blown_leads': 'sum'}
    blown_leads_single_season = blown_leads_single_season.groupby('team_abbrv').aggregate(aggregation_function)
    blown_leads_all_seasons_data = blown_leads_all_seasons_data.append(blown_leads_single_season)

blown_leads_all_seasons_data = blown_leads_all_seasons_data.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])
blown_leads_all_seasons_data_plot = blown_leads_all_seasons_data.plot(kind='bar')
# blown_leads_all_seasons_data_plot = blown_leads_all_seasons_data.iloc[0:50].plot(kind='bar')
plt.savefig('results/blown_leads_all_seasons_bar.png', bbox_inches='tight')

# range of blown leads for the league (with team id)
aggregation_function = {'blown_leads': 'sum'}
max_blown_leads_total_data_frame = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)
max_blown_leads_total = max_blown_leads_total_data_frame['blown_leads'].max()
max_blown_leads_total_data_frame = max_blown_leads_total_data_frame.where(max_blown_leads_total_data_frame['blown_leads'] == max_blown_leads_total).dropna()
min_blown_leads_total_data_frame = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)
min_blown_leads_total = min_blown_leads_total_data_frame['blown_leads'].min()
min_blown_leads_total_data_frame = min_blown_leads_total_data_frame.where(min_blown_leads_total_data_frame['blown_leads'] == min_blown_leads_total).dropna()

# range of blown leads for the league (with team id) per season
seasons = box_score_data_frame['season'].unique()
max_blown_leads_all_seasons = pd.DataFrame()
min_blown_leads_all_seasons = pd.DataFrame()
for season in seasons:
    season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)
    aggregation_function = {'blown_leads': 'sum'}
    season_data_frame = season_data_frame.groupby(['team_abbrv', 'season']).aggregate(aggregation_function)
    max_blown_leads_season = season_data_frame['blown_leads'].max()
    min_blown_leads_season = season_data_frame['blown_leads'].min()
    max_blown_leads_data = season_data_frame.where(season_data_frame['blown_leads'] == max_blown_leads_season).dropna()
    min_blown_leads_data = season_data_frame.where(season_data_frame['blown_leads'] == min_blown_leads_season).dropna()
    max_blown_leads_all_seasons = max_blown_leads_all_seasons.append(max_blown_leads_data)
    min_blown_leads_all_seasons = min_blown_leads_all_seasons.append(min_blown_leads_data)

# mean, median, mode, range of blown leads for the league
blown_leads_all_seasons_dict = {}
blown_leads_all_seasons_dict['mean'] = blown_leads_total_data['blown_leads'].mean()
blown_leads_all_seasons_dict['mode'] = blown_leads_total_data['blown_leads'].mode()[0]
blown_leads_all_seasons_dict['median'] = blown_leads_total_data['blown_leads'].median()
blown_leads_total_data_plot = blown_leads_total_data.plot(kind='box')
y_ticks = [tick for tick in range((blown_leads_total_data['blown_leads'].max()) + 1)]
blown_leads_total_data_plot.spines['right'].set_visible(False)
blown_leads_total_data_plot.spines['top'].set_visible(False)
blown_leads_total_data_plot.spines['left'].set_edgecolor('0.5')
blown_leads_total_data_plot.spines['left'].set_linewidth(1)
blown_leads_total_data_plot.spines['bottom'].set_edgecolor('0.5')
blown_leads_total_data_plot.spines['bottom'].set_linewidth(1)
plt.title(f'Total Blown Leads: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
plt.xlabel('All Teams', labelpad=10, fontsize=12)
# hide the x tick label
blown_leads_total_data_plot.set_xticklabels('')
plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
plt.yticks(y_ticks, fontsize=8)
plt.xticks(fontsize=8)
plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
plt.subplots_adjust(right=0.5)
plt.tight_layout()
plt.savefig('results/blown_leads_total_data_box_plot.png')

# mean, median, mode, range of blown leads for the league per season
seasons = list(box_score_data_frame['season'].unique())
teams = box_score_data_frame['team_abbrv'].unique()
blown_leads_per_season_data = pd.DataFrame(index=teams)
blown_leads_per_season_dict = {}

for season in seasons:
    # dataframe stuff
    blown_leads_single_season_data = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()
    aggregation_function = {'blown_leads': 'sum'}
    blown_leads_single_season_data = blown_leads_single_season_data.groupby('team_abbrv').aggregate(aggregation_function)
    blown_leads_single_season_data = blown_leads_single_season_data.rename(columns={'blown_leads': f'Blown Leads {season}'})
    blown_leads_per_season_data = blown_leads_per_season_data.merge(blown_leads_single_season_data, left_index=True, right_index=True)

    # stats dict stuff
    season_stats_dict = {}
    mean_blown_leads = blown_leads_single_season_data[f'Blown Leads {season}'].mean()
    mode_blown_leads = blown_leads_single_season_data[f'Blown Leads {season}'].mode()[0]
    median_blown_leads = blown_leads_single_season_data[f'Blown Leads {season}'].median()
    season_stats_dict['mean'] = mean_blown_leads
    season_stats_dict['mode'] = mode_blown_leads
    season_stats_dict['median'] = median_blown_leads
    blown_leads_per_season_dict[season] = season_stats_dict

blown_leads_per_season_data_plot = blown_leads_per_season_data.plot(kind='box')
blown_leads_per_season_data_plot.spines['right'].set_visible(False)
blown_leads_per_season_data_plot.spines['top'].set_visible(False)
blown_leads_per_season_data_plot.spines['left'].set_edgecolor('0.5')
blown_leads_per_season_data_plot.spines['left'].set_linewidth(1)
blown_leads_per_season_data_plot.spines['bottom'].set_edgecolor('0.5')
blown_leads_per_season_data_plot.spines['bottom'].set_linewidth(1)
plt.title(f'Total Blown Leads\nfor each Season: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
plt.xlabel('Seasons', labelpad=10, fontsize=12)
blown_leads_per_season_data_plot.set_xticklabels(seasons)
plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
plt.yticks(y_ticks, fontsize=8)
plt.xticks(fontsize=8)
plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
plt.subplots_adjust(right=0.5)
plt.tight_layout()
plt.savefig('results/blown_leads_per_season_box_plot.png')

# mean, median, mode, range of blown leads for STL
stl_blown_leads_data = pd.DataFrame(blown_leads_per_season_data.loc['STL'])
stl_blown_leads_data_plot = stl_blown_leads_data.plot(kind='box')

stl_blown_leads_data_plot.spines['right'].set_visible(False)
stl_blown_leads_data_plot.spines['top'].set_visible(False)
stl_blown_leads_data_plot.spines['left'].set_edgecolor('0.5')
stl_blown_leads_data_plot.spines['left'].set_linewidth(1)
stl_blown_leads_data_plot.spines['bottom'].set_edgecolor('0.5')
stl_blown_leads_data_plot.spines['bottom'].set_linewidth(1)
plt.title(f'Total Blown Leads for the St. Louis Cardinals: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
plt.xlabel('STL', labelpad=10, fontsize=12)
stl_blown_leads_data_plot.set_xticklabels('')
plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
plt.yticks(y_ticks, fontsize=8)
plt.xticks(fontsize=8)
plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
# plt.subplots_adjust(right=0.5)
# plt.tight_layout()
plt.savefig('results/stl_blown_leads.png', bbox_inches='tight')

stl_blown_leads_stats_dict = {}
stl_blown_leads = blown_leads_per_season_data.loc['STL']

blown_leads_max = stl_blown_leads.max()
blown_leads_max_season = stl_blown_leads.idxmax()
stl_blown_leads_stats_dict['maximum'] = {blown_leads_max_season: blown_leads_max}

blown_leads_min = stl_blown_leads.min()
blown_leads_min_season = stl_blown_leads.idxmin()

stl_blown_leads_stats_dict['minimum'] = {blown_leads_min_season: blown_leads_min}
stl_blown_leads_stats_dict['mean'] = stl_blown_leads.mean()
stl_blown_leads_stats_dict['mode'] = list(stl_blown_leads.mode())
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
    aggregation_function = {'blown_leads': 'sum'}
    stl_blown_leads_single_season_data = stl_blown_leads_single_season_data.groupby('team_abbrv').aggregate(aggregation_function)
    stl_blown_leads_single_season = list(stl_blown_leads_single_season_data.iloc[0])[0]
    stl_blown_leads_lead_losses_per_season[season] = stl_blown_leads_single_season

stl_blown_leads_lead_mean_per_season = list(stl_blown_leads_lead_losses_per_season.values())
stl_blown_leads_lead_mean_per_season = statistics.mean(stl_blown_leads_lead_mean_per_season)

stl_blown_leads_all_seasons_data_dict['total'] = stl_blown_leads_lead_losses_total
stl_blown_leads_all_seasons_data_dict['mean'] = stl_blown_leads_lead_mean_per_season
stl_blown_leads_all_seasons_data_dict['seasons'] = stl_blown_leads_lead_losses_per_season


with open('results/results.txt', 'w') as f:
    seasons = box_score_data_frame['season'].unique()
    max_blown_leads_total_string = 'Maximum blown leads for any major league baseball team, seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(max_blown_leads_total) + '\n'
    min_blown_leads_total_string = 'Minimum blown leads for any major league baseball team, seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(min_blown_leads_total) + '\n'
    f.write(max_blown_leads_total_string)
    f.write('Data for team(s) with the most blown leads for all seasons from ' + seasons[0] + '-' + seasons[-1] + ':\n')
    f.write(str(max_blown_leads_total_data_frame) + '\n')
    f.write('\n')
    f.write(min_blown_leads_total_string)
    f.write('Data for team(s) with the fewest blown leads for all seasons from ' + seasons[0] + '-' + seasons[-1] + ':\n')
    f.write(str(min_blown_leads_total_data_frame) + '\n\n')
    f.write('Data on the mean, median, and mode blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ':\n')
    f.write('Mean number of blown leads: ' + str(blown_leads_all_seasons_dict['mean']) + '\n')
    f.write('Mode number of blown leads: ' + str(blown_leads_all_seasons_dict['mode']) + '\n')
    f.write('Median number of blown leads: ' + str(blown_leads_all_seasons_dict['median']) + '\n\n')
    f.write('Data for the team(s) with the most blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
    f.write(str(max_blown_leads_all_seasons) + '\n\n')
    f.write('Data for the team(s) with the fewest blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
    f.write(str(min_blown_leads_all_seasons) + '\n\n')
    f.write('Data on the mean, mode, and median blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
    for season in seasons:
        f.write(season + ' Data:\n')
        f.write('\tMean: ' + str(blown_leads_per_season_dict[season]['mean']) + '\n')
        f.write('\tMode: ' + str(blown_leads_per_season_dict[season]['mode']) + '\n')
        f.write('\tMedian: ' + str(blown_leads_per_season_dict[season]['median']) + '\n\n')
    f.write('St. Louis Cardinals Blown Leads Data:\n')
    f.write('\tAverage number of blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_leads_stats_dict['mean']) + '\n')
    f.write('\tSeason with the most blown leads: ' + str(stl_blown_leads_stats_dict['maximum']) + '\n')
    f.write('\tSeason with the fewest blown leads: ' + str(stl_blown_leads_stats_dict['minimum']) + '\n\n')
    f.write('Data on the mean, mode, and median blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ':\n')
    f.write('\tMean: ' + str(stl_blown_leads_stats_dict['mean']) + '\n')
    f.write('\tMode: ' + str(stl_blown_leads_stats_dict['mode']) + '\n')
    f.write('\tMedian: ' + str(stl_blown_leads_stats_dict['median']) + '\n\n')
    f.write('Data on games where the St. Louis Cardinals blew at least one lead and lost:\n')
    f.write('\tTotal number of "blown lead losses" for the St. Louis Cardinals from seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_leads_all_seasons_data_dict['total']) + '\n')
    f.write('\tAverage number of "blown lead losses" for the St. Louis Cardinals per season from ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_leads_all_seasons_data_dict['mean']) + '\n')
    f.write('\tNumber of "blown lead losses" from ' + seasons[0] + '-' + seasons[-1] + ':\n')
    for season in seasons:
        f.write('\t\t' + season + ' Blown Lead Losses: ' + str(stl_blown_leads_all_seasons_data_dict['seasons'][season]) + '\n')

end_time = datetime.datetime.now()
print(f'Total Time: {end_time - start_time}')
