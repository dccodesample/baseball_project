# TODO: re-organize code, logging, Error handling, formatting, efficiency, clarity, comment code last
import json
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams["font.family"] = "Verdana"
from src.BoxScore import BoxScore
import time
import statistics
from utils.box_score_data_analysis_utils import BoxScoreDataAnalysisUtils
import logging


# sets up the python logging object
logging.basicConfig(format='%(asctime)s - %(filename)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()
logger.info('STARTING: Data Analysis')

# collects box score data
logger.info('STARTING: Collecting box score data')
data_analysis_utils_object = BoxScoreDataAnalysisUtils('data/box_score_data_small.json')
box_score_data = data_analysis_utils_object.get_box_score_data()
logger.info('FINISHED: Collecting box score data')

# converting box score data to Box Score objects and storing the objects in a pandas data frame
logger.info('STARTING: Converting to Box Score objects and storing in a pandas dataframe')
box_score_data_frame = data_analysis_utils_object.convert_box_score_data_to_dataframe(box_score_data)
# with pd.option_context('display.max_columns', 2000):  # DELETE
#     with open('test_file.txt', 'w') as f:  # DELETE
#         f.write(str(box_score_data_frame))  # DELETE
logger.info('FINISHED: Converting to Box Score objects and storing in a pandas dataframe')

# Calculating the number of seasons in the data frame
logger.info('STARTING: Calculating the number of seasons in the data frame')
seasons = data_analysis_utils_object.calculate_seasons(box_score_data_frame)
logger.info('FINISHED: Calculating the number of seasons in the data frame')

# Calculating the number of total blown leads per team
logger.info('STARTING: Preparing total blown leads data')
blown_leads_total_data_frame = data_analysis_utils_object.calculate_total_blown_leads(box_score_data_frame)
logger.info('FINISHED: Preparing total blown leads data')

# Creating a bar chart of total blown leads per team
logger.info('STARTING: Charting total blown leads data (bar chart)')
data_analysis_utils_object.plot_total_blown_leads_bar_chart(blown_leads_total_data_frame, seasons)
logger.info('FINISHED: Charting total blown leads data (bar chart)')

# Calculating the number of blown leads per team for each season
logger.info('STARTING: Preparing total blown leads for each team and season data')
blown_leads_per_team_season_data_frame = data_analysis_utils_object.calculate_total_blown_leads_per_team_season(box_score_data_frame, seasons)
logger.info('FINISHED: Preparing total blown leads for each team and season data')

# Creating a bar chart of the most blown leads by any team in a season
logger.info('STARTING: Charting the most blown leads by any team in a season (bar chart)')
data_analysis_utils_object.plot_most_blown_leads_per_team_season_bar_chart(blown_leads_per_team_season_data_frame, seasons)
logger.info('FINISHED: Charting the most blown leads by any team in a season (bar chart)')

# Calculating the maximum and minimum number of blown leads by a team over the study period
logger.info('STARTING: Preparing maximum and minimum number of blown leads for all seasons data')
max_blow_leads_total = data_analysis_utils_object.calculate_max_blown_leads_total(box_score_data_frame)
max_blow_leads_total_data_frame = data_analysis_utils_object.create_max_blown_leads_tota_data_frame(box_score_data_frame, max_blow_leads_total)  # finds the name of the team who had the maximum number of blown leads
min_blow_leads_total = data_analysis_utils_object.calculate_min_blown_leads_total(box_score_data_frame)
min_blow_leads_total_data_frame = data_analysis_utils_object.create_min_blown_leads_tota_data_frame(box_score_data_frame, min_blow_leads_total)  # finds the name of the team who had the minimum number of blown leads
logger.info('FINISHED: Preparing maximum and minimum number of blown leads for all seasons data')

# Calculating the maximum and minimum number of blown leads by a team for each season
logger.info('STARTING: Preparing maximum and minimum number of blown leads for each season data')
max_blown_leads_per_season = data_analysis_utils_object.calculate_max_blown_leads_per_season(box_score_data_frame, seasons)
max_blown_leads_per_season_data_frame = data_analysis_utils_object.create_max_blown_leads_per_season_data_frame(box_score_data_frame, max_blown_leads_per_season, seasons)
min_blown_leads_per_season = data_analysis_utils_object.calculate_min_blown_leads_per_season(box_score_data_frame, seasons)
min_blown_leads_per_season_data_frame = data_analysis_utils_object.create_min_blown_leads_per_season_data_frame(box_score_data_frame, min_blown_leads_per_season, seasons)
logger.info('FINISHED: Preparing maximum and minimum number of blown leads for each season data')

# Calculating the mean, median, and mode for the blown leads data for the entire study period
logger.info('STARTING: Calculating the mean, median, and mode for the blown leads data for the entire study period')
blown_leads_all_seasons_dict = {}
blown_leads_all_seasons_dict['mean'] = blown_leads_total_data_frame['blown_leads'].mean()
blown_leads_all_seasons_dict['mode'] = blown_leads_total_data_frame['blown_leads'].mode()[0]
blown_leads_all_seasons_dict['median'] = blown_leads_total_data_frame['blown_leads'].median()
logger.info('FINISHED: Calculating the mean, median, and mode for the blown leads data for the entire study period')

# Creating a box plot of total blown leads per team
logger.info('STARTING: Charting total blown leads data (box plot)')
data_analysis_utils_object.plot_total_blown_leads_box_plot(blown_leads_total_data_frame, seasons)
logger.info('FINISHED: Charting total blown leads data (box plot)')


# # mean, median, mode, range of blown leads for the league per season
# seasons = list(box_score_data_frame['season'].unique())
# teams = box_score_data_frame['team_abbrv'].unique()
# blown_leads_per_season_data = pd.DataFrame(index=teams)
# blown_leads_per_season_dict = {}

# for season in seasons:
#     # dataframe stuff
#     blown_leads_single_season_data = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()
#     aggregation_function = {'blown_leads': 'sum'}
#     blown_leads_single_season_data = blown_leads_single_season_data.groupby('team_abbrv').aggregate(aggregation_function)
#     blown_leads_single_season_data = blown_leads_single_season_data.rename(columns={'blown_leads': f'Blown Leads {season}'})
#     blown_leads_per_season_data = blown_leads_per_season_data.merge(blown_leads_single_season_data, left_index=True, right_index=True)

#     # stats dict stuff
#     season_stats_dict = {}
#     mean_blown_leads = blown_leads_single_season_data[f'Blown Leads {season}'].mean()
#     mode_blown_leads = blown_leads_single_season_data[f'Blown Leads {season}'].mode()[0]
#     median_blown_leads = blown_leads_single_season_data[f'Blown Leads {season}'].median()
#     season_stats_dict['mean'] = mean_blown_leads
#     season_stats_dict['mode'] = mode_blown_leads
#     season_stats_dict['median'] = median_blown_leads
#     blown_leads_per_season_dict[season] = season_stats_dict

# blown_leads_per_season_data_plot = blown_leads_per_season_data.plot(kind='box')
# blown_leads_per_season_data_plot.spines['right'].set_visible(False)
# blown_leads_per_season_data_plot.spines['top'].set_visible(False)
# blown_leads_per_season_data_plot.spines['left'].set_edgecolor('0.5')
# blown_leads_per_season_data_plot.spines['left'].set_linewidth(1)
# blown_leads_per_season_data_plot.spines['bottom'].set_edgecolor('0.5')
# blown_leads_per_season_data_plot.spines['bottom'].set_linewidth(1)
# plt.title(f'Total Blown Leads\nfor each Season: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
# plt.xlabel('Seasons', labelpad=10, fontsize=12)
# blown_leads_per_season_data_plot.set_xticklabels(seasons)
# plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
# max_blown_leads_per_season_list = []
# for season in seasons:
#     max_blown_leads_per_season_list.append(blown_leads_per_season_data[f'Blown Leads {season}'].max())
# max_blown_leads_per_season = int(max(max_blown_leads_per_season_list))
# y_ticks = calculate_y_ticks(max_blown_leads_per_season)
# plt.yticks(y_ticks, fontsize=8)
# plt.xticks(fontsize=8)
# plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
# plt.subplots_adjust(right=0.5)
# plt.tight_layout()
# plt.savefig('results/blown_leads_per_season_box_plot.png')

# GET TO HERE

# # mean, median, mode, range of blown leads for STL
# stl_blown_leads_data = pd.DataFrame(blown_leads_per_season_data.loc['STL'])
# stl_blown_leads_data_plot = stl_blown_leads_data.plot(kind='box')

# stl_blown_leads_data_plot.spines['right'].set_visible(False)
# stl_blown_leads_data_plot.spines['top'].set_visible(False)
# stl_blown_leads_data_plot.spines['left'].set_edgecolor('0.5')
# stl_blown_leads_data_plot.spines['left'].set_linewidth(1)
# stl_blown_leads_data_plot.spines['bottom'].set_edgecolor('0.5')
# stl_blown_leads_data_plot.spines['bottom'].set_linewidth(1)
# plt.title(f'Total Blown Leads for the St. Louis Cardinals: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
# plt.xlabel('STL', labelpad=10, fontsize=12)
# stl_blown_leads_data_plot.set_xticklabels('')
# plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
# stl_max_blown_leads = int(stl_blown_leads_data['STL'].max())
# y_ticks = calculate_y_ticks(stl_max_blown_leads)
# plt.yticks(y_ticks, fontsize=8)
# plt.xticks(fontsize=8)
# plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
# plt.savefig('results/stl_blown_leads.png', bbox_inches='tight')

# stl_blown_leads_stats_dict = {}
# stl_blown_leads = blown_leads_per_season_data.loc['STL']

# blown_leads_max = stl_blown_leads.max()
# blown_leads_max_season = stl_blown_leads.idxmax()
# stl_blown_leads_stats_dict['maximum'] = {blown_leads_max_season: blown_leads_max}

# blown_leads_min = stl_blown_leads.min()
# blown_leads_min_season = stl_blown_leads.idxmin()

# stl_blown_leads_stats_dict['minimum'] = {blown_leads_min_season: blown_leads_min}
# stl_blown_leads_stats_dict['mean'] = stl_blown_leads.mean()
# stl_blown_leads_stats_dict['mode'] = list(stl_blown_leads.mode())
# stl_blown_leads_stats_dict['median'] = stl_blown_leads.median()

# # number of times STL blew at least 1 lead and lost
# seasons = box_score_data_frame['season'].unique()
# stl_blown_leads_all_seasons_data_dict = {}
# stl_blown_leads_data = box_score_data_frame.where(
#     (box_score_data_frame['team_abbrv'] == 'STL') &
#     (box_score_data_frame['blown_leads'] > 0) &
#     (box_score_data_frame['result'] == 0)
# ).dropna()

# stl_blown_leads_lead_losses_total = len(stl_blown_leads_data.index)
# stl_blown_leads_lead_losses_per_season = {}
# for season in seasons:
#     stl_blown_leads_single_season_data = stl_blown_leads_data.where(stl_blown_leads_data['season'] == season).dropna()
#     aggregation_function = {'blown_leads': 'sum'}
#     stl_blown_leads_single_season_data = stl_blown_leads_single_season_data.groupby('team_abbrv').aggregate(aggregation_function)
#     stl_blown_leads_single_season = list(stl_blown_leads_single_season_data.iloc[0])[0]
#     stl_blown_leads_lead_losses_per_season[season] = stl_blown_leads_single_season

# stl_blown_leads_lead_mean_per_season = list(stl_blown_leads_lead_losses_per_season.values())
# stl_blown_leads_lead_mean_per_season = statistics.mean(stl_blown_leads_lead_mean_per_season)

# stl_blown_leads_all_seasons_data_dict['total'] = stl_blown_leads_lead_losses_total
# stl_blown_leads_all_seasons_data_dict['mean'] = stl_blown_leads_lead_mean_per_season
# stl_blown_leads_all_seasons_data_dict['seasons'] = stl_blown_leads_lead_losses_per_season


# with open('results/results.txt', 'w') as f:
#     seasons = box_score_data_frame['season'].unique()
#     max_blown_leads_total_string = 'Maximum blown leads for any major league baseball team, seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(max_blown_leads_total) + '\n'
#     min_blown_leads_total_string = 'Minimum blown leads for any major league baseball team, seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(min_blown_leads_total) + '\n'
#     f.write(max_blown_leads_total_string)
#     f.write('Data for team(s) with the most blown leads for all seasons from ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     f.write(str(max_blown_leads_total_data_frame) + '\n')
#     f.write('\n')
#     f.write(min_blown_leads_total_string)
#     f.write('Data for team(s) with the fewest blown leads for all seasons from ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     f.write(str(min_blown_leads_total_data_frame) + '\n\n')
#     f.write('Data on the mean, median, and mode blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     f.write('Mean number of blown leads: ' + str(blown_leads_all_seasons_dict['mean']) + '\n')
#     f.write('Mode number of blown leads: ' + str(blown_leads_all_seasons_dict['mode']) + '\n')
#     f.write('Median number of blown leads: ' + str(blown_leads_all_seasons_dict['median']) + '\n\n')
#     f.write('Data for the team(s) with the most blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     f.write(str(max_blown_leads_all_seasons) + '\n\n')
#     f.write('Data for the team(s) with the fewest blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     f.write(str(min_blown_leads_all_seasons) + '\n\n')
#     f.write('Data on the mean, mode, and median blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     for season in seasons:
#         f.write(season + ' Data:\n')
#         f.write('\tMean: ' + str(blown_leads_per_season_dict[season]['mean']) + '\n')
#         f.write('\tMode: ' + str(blown_leads_per_season_dict[season]['mode']) + '\n')
#         f.write('\tMedian: ' + str(blown_leads_per_season_dict[season]['median']) + '\n\n')
#     f.write('St. Louis Cardinals Blown Leads Data:\n')
#     f.write('\tAverage number of blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_leads_stats_dict['mean']) + '\n')
#     f.write('\tSeason with the most blown leads: ' + str(stl_blown_leads_stats_dict['maximum']) + '\n')
#     f.write('\tSeason with the fewest blown leads: ' + str(stl_blown_leads_stats_dict['minimum']) + '\n\n')
#     f.write('Data on the mean, mode, and median blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     f.write('\tMean: ' + str(stl_blown_leads_stats_dict['mean']) + '\n')
#     f.write('\tMode: ' + str(stl_blown_leads_stats_dict['mode']) + '\n')
#     f.write('\tMedian: ' + str(stl_blown_leads_stats_dict['median']) + '\n\n')
#     f.write('Data on games where the St. Louis Cardinals blew at least one lead and lost:\n')
#     f.write('\tTotal number of "blown lead losses" for the St. Louis Cardinals from seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_leads_all_seasons_data_dict['total']) + '\n')
#     f.write('\tAverage number of "blown lead losses" for the St. Louis Cardinals per season from ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_leads_all_seasons_data_dict['mean']) + '\n')
#     f.write('\tNumber of "blown lead losses" from ' + seasons[0] + '-' + seasons[-1] + ':\n')
#     for season in seasons:
#         f.write('\t\t' + season + ' Blown Lead Losses: ' + str(stl_blown_leads_all_seasons_data_dict['seasons'][season]) + '\n')

