# TODO: re-organize code, logging, Error handling, formatting, efficiency, clarity, comment code last
import pandas as pd
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

# Calculating the number of seasons and teams in the data frame
logger.info('STARTING: Calculating the number of seasons and teams in the data frame')
seasons = data_analysis_utils_object.calculate_seasons(box_score_data_frame)
team_abbrvs = data_analysis_utils_object.calculate_team_abbrvs(box_score_data_frame)
logger.info('FINISHED: Calculating the number of seasons and teams in the data frame')

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
max_blown_leads_total = data_analysis_utils_object.calculate_max_blown_leads_total(box_score_data_frame)
max_blown_leads_total_data_frame = data_analysis_utils_object.create_max_blown_leads_tota_data_frame(box_score_data_frame, max_blown_leads_total)  # finds the name of the team who had the maximum number of blown leads
min_blown_leads_total = data_analysis_utils_object.calculate_min_blown_leads_total(box_score_data_frame)
min_blown_leads_total_data_frame = data_analysis_utils_object.create_min_blown_leads_tota_data_frame(box_score_data_frame, min_blown_leads_total)  # finds the name of the team who had the minimum number of blown leads
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

# Collecting blown leads data for each team for each season
logger.info('STARTING: Collecting the blown leads data for each team for each season')
blown_leads_per_season_data_frame = data_analysis_utils_object.create_blown_leads_per_season_data_frame(box_score_data_frame, seasons, team_abbrvs)
logger.info('FINISHED: Collecting the blown leads data for each team for each season')

# Calculating the mean, median, and mode for the blown leads data for each season
logger.info('STARTING: Calculating the mean, median, and mode for the blown leads data for each seasons')
blown_leads_per_season_dict = data_analysis_utils_object.calcuate_blown_lead_descriptive_stats_per_season(blown_leads_per_season_data_frame)
logger.info('FINISHED: Calculating the mean, median, and mode for the blown leads data for each seasons')

# Creating a box plot of blown leads per team for each season
logger.info('STARTING: Charting the number of blown leads per team for each season (box plot)')
data_analysis_utils_object.plot_per_season_blown_leads_box_plot(blown_leads_per_season_data_frame, seasons)
logger.info('FINISHED: Charting the number of blown leads per team for each season (box plot)')

# Collecting blown leads data for the St. Louis Cardinals
logger.info('STARTING: Collecting blown leads data for the St. Louis Cardinals')
blown_leads_stl_data_frame = pd.DataFrame(blown_leads_per_season_data_frame.loc['STL'])
logger.info('FINISHED: Collecting blown leads data for the St. Louis Cardinals')

# Creating a box plot of the number blown leads for the St. Louis Cardinals for each season
logger.info('STARTING: Charting the number blown leads for the St. Louis Cardinals for each season')
data_analysis_utils_object.plot_stl_blown_leads_box_plot(blown_leads_stl_data_frame, seasons)
logger.info('FINISHED: Charting the number blown leads for the St. Louis Cardinals for each season')

# Calculating descriptive statistics for the St. Louis blown leads data
logger.info('STARTING: Calculating descriptive statistics for the St. Louis blown leads data')
blown_leads_stl_stats_dict = data_analysis_utils_object.calcuate_blown_lead_descriptive_stats_stl(blown_leads_stl_data_frame)
logger.info('FINISHED: Calculating descriptive statistics for the St. Louis blown leads data')

# Collecting blown lead lossess data for the St. Louis Cardinals
logger.info('STARTING: Collecting blown lead losses data for the St. Louis Cardinals')
blown_lead_losses_stl_data_frame = box_score_data_frame.where(
    (box_score_data_frame['team_abbrv'] == 'STL') &
    (box_score_data_frame['blown_leads'] > 0) &
    (box_score_data_frame['result'] == 0)
).dropna()
logger.info('FINISHED: Collecting blown lead losses data for the St. Louis Cardinals')

# Calculating descriptive statistics for the St. Louis blown lead losses data
logger.info('STARTING: Calculating descriptive statistics for the St. Louis blown lead losses data')
stl_blown_lead_losses_stats_dict = data_analysis_utils_object.calcuate_blown_lead_losses_descriptive_stats_stl(blown_lead_losses_stl_data_frame, seasons)
logger.info('FINISHED: Calculating descriptive statistics for the St. Louis blown lead losses data')

# Writing results to a text file
logger.info('STARTING: Writing results to a text file')
data_analysis_utils_object.output_results(box_score_data_frame, max_blown_leads_total, min_blown_leads_total, max_blown_leads_total_data_frame,
                                          min_blown_leads_total_data_frame, blown_leads_all_seasons_dict, max_blown_leads_per_season_data_frame,
                                          min_blown_leads_per_season_data_frame, blown_leads_per_season_dict, blown_leads_stl_stats_dict,
                                          stl_blown_lead_losses_stats_dict)
logger.info('FINISHED: Writing results to a text file')

logger.info('FINISHED: Data Analysis')
