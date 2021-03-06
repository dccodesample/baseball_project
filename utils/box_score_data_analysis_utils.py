import json
import pandas as pd
import statistics
from matplotlib import pyplot as plt
from src.BoxScore import BoxScore
plt.rcParams["font.family"] = "Verdana"


class BoxScoreDataAnalysisUtils:
    """A class with a collection of utility methods that perform data analysis on the box score data generated in the box_score_data_collection.py program.

    Attributes:
        self.box_score_data_uri: the path to the data file containing the box score data.
    """

    def __init__(self, box_score_data_uri):
        """Initializes BoxScoreDataAnalysisUtils with self.box_score_data_uri."""

        self.box_score_data_uri = box_score_data_uri

    def calcuate_blown_lead_descriptive_stats_per_season(self, blown_leads_per_season_data_frame):
        """Calculates the mean, median, and mode of blown leads for each season, and stores the data in a dictionary.

        Args:
            blown_leads_per_season_data_frame: the data frame containing the number of blown leads per team for each season, as created in the create_blown_leads_per_season_data_frame method

        Returns:
            Returns a dictionary, mapping each season to the mean, median, and mode for that year. For example:

            {
            '2012': {
                'mean': 0.1, 'mode': 0.0, 'median': 0.0
                },
            '2013': {
                'mean': 0.1, 'mode': 0.0, 'median': 0.0
                }
            }
        """

        blown_leads_per_season_dict = {}  # the dictionary which will store the mean, median, and mode for all seasons
        index = 0

        for column in blown_leads_per_season_data_frame:
            season = column[-4:]  # finds the season number

            season_stats_dict = {}  # the season dictionary, which will store the mean, median, and mode for the season

            # calculates the mean, median, and mode for the season
            mean_blown_leads = blown_leads_per_season_data_frame[column].mean()
            mode_blown_leads = blown_leads_per_season_data_frame[column].mode()[0]
            median_blown_leads = blown_leads_per_season_data_frame[column].median()

            # stores the data for the season
            season_stats_dict['mean'] = mean_blown_leads
            season_stats_dict['mode'] = mode_blown_leads
            season_stats_dict['median'] = median_blown_leads
            blown_leads_per_season_dict[season] = season_stats_dict

            index += 1

        return blown_leads_per_season_dict

    def calcuate_blown_lead_descriptive_stats_stl(self, blown_leads_stl_data_frame):
        """Calcuates descriptive statistics (range, mean, median, mode) on the blown leads data for the St. Louis Cardinals.

        Args:
            blown_leads_stl_data_frame: the data frame containing the number of blown leads per from each season for the St. Louis Cardinals

        Returns:
            Returns a dictionary containing the maximum, minimum, mean, median, and mode of the blown leads data for the St. Louis Cardinals.
            For example:

            {'maximum': {'Blown Leads 2012': 1}, 'minimum': {'Blown Leads 2012': 1}, 'mean': 1, 'mode': array([[1.]]), 'median': 1}

        """
        stl_blown_leads_stats_dict = {}  # the dictionary that will store the descriptive statistics

        # calcuates the maximum number of blown leads in a season
        blown_leads_max = int(blown_leads_stl_data_frame.max())
        blown_leads_max_season = blown_leads_stl_data_frame.idxmax()[0]
        stl_blown_leads_stats_dict['maximum'] = {blown_leads_max_season: blown_leads_max}

        # calcuates the minimum number of blown leads in a season
        blown_leads_min = int(blown_leads_stl_data_frame.min())
        blown_leads_min_season = blown_leads_stl_data_frame.idxmin()[0]
        stl_blown_leads_stats_dict['minimum'] = {blown_leads_min_season: blown_leads_min}

        # calcuates the mean, median, and mode number of blown leads in a season
        stl_blown_leads_stats_dict['mean'] = int(blown_leads_stl_data_frame.mean())
        stl_blown_leads_stats_dict['mode'] = blown_leads_stl_data_frame.mode().values
        stl_blown_leads_stats_dict['median'] = int(blown_leads_stl_data_frame.median())

        return stl_blown_leads_stats_dict

    def calcuate_blown_lead_losses_descriptive_stats_stl(self, blown_lead_losses_stl_data_frame, seasons):
        """Calculates descriptive statistics on the number of games where the St. Louis Cardinals blew a lead and lost, for each season in the study period.

        Args:
            blown_lead_losses_stl_data_frame: a dataframe containing descriptive information on the games where the St. Louis Cardinals blew a lead and lost
            seasons: a list the number of seasons in the study

        Returns:
            Returns a dictionary with descriptive statistics on the number of blown lead losses for the St. Louis Cardinals across the study period.
            For example:

                {
                    'total': 2,
                    'mean': 1.0,
                    'seasons': {
                        '2012': 1.0,
                        '2013': 1.0
                    }
                }
        """

        stl_blown_leads_all_seasons_data_dict = {}  # the dicionary that will hold the all the statistics for all seasons
        stl_blown_leads_lead_losses_per_season = {}  # sub-dictionary which holds the number of blown lead losses for each season

        stl_blown_leads_lead_losses_total = len(blown_lead_losses_stl_data_frame.index)

        for season in seasons:
            # collects data for the given season
            stl_blown_leads_single_season_data = blown_lead_losses_stl_data_frame.where(blown_lead_losses_stl_data_frame['season'] == season).dropna()

            # calculates the number of blown lead losses for the season
            aggregation_function = {'blown_leads': 'sum'}
            stl_blown_leads_single_season_data = stl_blown_leads_single_season_data.groupby('team_abbrv').aggregate(aggregation_function)

            # stores the results in the respoective dictionaries
            stl_blown_leads_single_season = list(stl_blown_leads_single_season_data.iloc[0])[0]
            stl_blown_leads_lead_losses_per_season[season] = stl_blown_leads_single_season

        # calculates the mean number of blown lead losses across all seasons
        stl_blown_lead_losses_total_mean = list(stl_blown_leads_lead_losses_per_season.values())
        stl_blown_lead_losses_total_mean = statistics.mean(stl_blown_lead_losses_total_mean)

        # stores the data
        stl_blown_leads_all_seasons_data_dict['total'] = stl_blown_leads_lead_losses_total
        stl_blown_leads_all_seasons_data_dict['mean'] = stl_blown_lead_losses_total_mean
        stl_blown_leads_all_seasons_data_dict['seasons'] = stl_blown_leads_lead_losses_per_season

        return stl_blown_leads_all_seasons_data_dict

    def calculate_max_blown_leads_per_season(self, box_score_data_frame, seasons):
        """Calculates the largerst number of leads a team blew for each season.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            seasons: a list the number of seasons in the study

        Returns:
            Returns a dictionary that maps each season to the largest number of leads blown in that season. For example,

            {'2012': 1.0, '2013': 1.0}
        """

        max_blown_leads_per_season_dict = {}

        for season in seasons:
            # collects the box score data for the season
            season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)

            # calculates the number of blown leads for that season
            aggregation_function = {'blown_leads': 'sum'}
            season_data_frame = season_data_frame.groupby(['team_abbrv', 'season']).aggregate(aggregation_function)

            # finds the maximum number of blown leads for that season
            max_blown_leads_season_dict = season_data_frame['blown_leads'].max()

            # stores the maximum number of blown leads for that season, in the dictionary containing the data for all seasons
            max_blown_leads_per_season_dict[season] = max_blown_leads_season_dict

        return max_blown_leads_per_season_dict

    def calculate_max_blown_leads_total(self, box_score_data_frame):
        """Calculates the largerst number of leads a team blew in total (across the study period).

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method

        Returns:
            Returns an numpy integer representing the largerst number of leads a team blew in total (across the study period)
        """

        # calculates the number of leads each team blew
        aggregation_function = {'blown_leads': 'sum'}
        max_blown_leads_total_data_frame = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)

        max_blown_leads_total = max_blown_leads_total_data_frame['blown_leads'].max()  # finds the maximum number of blown leads

        return max_blown_leads_total

    def calculate_min_blown_leads_per_season(self, box_score_data_frame, seasons):
        """Calculates the smallest number of leads a team blew for each season.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            seasons: a list the number of seasons in the study

        Returns:
            Returns a dictionary that maps each season to the smallest number of leads blown in that season. For example,

            {'2012': 0.0, '2013': 0.0}
        """

        min_blown_leads_per_seasons_dict = {}

        for season in seasons:
            # collects the box score data for the season
            season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)

            # calculates the number of blown leads for that season
            aggregation_function = {'blown_leads': 'sum'}
            season_data_frame = season_data_frame.groupby(['team_abbrv', 'season']).aggregate(aggregation_function)

            # finds the minimum number of blown leads for that season
            min_blown_leads_season_dict = season_data_frame['blown_leads'].min()

            # stores the minimum number of blown leads for that season, in the dictionary containing the data for all seasons
            min_blown_leads_per_seasons_dict[season] = min_blown_leads_season_dict

        return min_blown_leads_per_seasons_dict

    def calculate_min_blown_leads_total(self, box_score_data_frame):
        """Calculates the smallest number of leads a team blew in total (across the study period).

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method

        Returns:
            Returns an numpy integer representing the smallest number of leads a team blew in total (across the study period)
        """

        # calculates the number of leads each team blew
        aggregation_function = {'blown_leads': 'sum'}
        min_blown_leads_total_data_frame = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)

        min_blown_leads_total = min_blown_leads_total_data_frame['blown_leads'].min()  # finds the minimum number of blown leads

        return min_blown_leads_total

    def calculate_seasons(self, box_score_data_frame):
        """Finds the number of seasons in the dataframe (i.e., the number of seasons in the study).

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method

        Returns:
            Returns a list of the seasons in the study. For example,

            [2012, 2013]
        """

        seasons = list(box_score_data_frame['season'].unique())
        return seasons

    def calculate_team_abbrvs(self, box_score_data_frame):
        """Finds the team abbreviations in the dataframe.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method

        Returns:
            Returns a list of the team abbreviations in the study. For example,

            ['ARI', 'ATL', 'BAL']
        """

        team_abbrvs = list(box_score_data_frame['team_abbrv'].unique())
        return team_abbrvs

    def calculate_total_blown_leads(self, box_score_data_frame):
        """Calculates the total number of leads each team blew for all seasons.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method

        Returns:
            Returns a pandas dataframe where the index is team abbreviation, and the only column is the number of blown leads. For example:

                            blown_leads
                team_abbrv
                CLE                   1
                TBR                   1
                ARI                   0
        """

        # calculates the number of blown leads for each team
        aggregation_function = {'blown_leads': 'sum'}
        blown_leads_total_data = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)

        # sorts the data by blown leads (descending) and then alphabetically (ascending)
        blown_leads_total_data = blown_leads_total_data.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])

        return blown_leads_total_data

    def calculate_total_blown_leads_per_team_season(self, box_score_data_frame, seasons):
        """Calculates the number of leads each team blew for each season in seasons.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            seasons: a list the number of seasons in the study

        Returns:
            Returns a pandas dataframe where the index is team abbreviation and season number, and the only column is the number of blown leads for that season.
            For example:

                        blown_leads
            team_abbrv
            ARI 2012            0.0
            ATL 2012            0.0
            BAL 2012            0.0
        """

        blown_leads_all_seasons_data = pd.DataFrame()

        for season in seasons:
            # collects values only from the given seasons
            blown_leads_single_season = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()

            # renames the values in the 'team_abbrv' column to include the season number
            blown_leads_single_season['team_abbrv'] = blown_leads_single_season['team_abbrv'].apply(lambda x: f'{x} {season}')

            # calculates the number of blown leads for each team for that season
            aggregation_function = {'blown_leads': 'sum'}
            blown_leads_single_season = blown_leads_single_season.groupby('team_abbrv').aggregate(aggregation_function)  # creates a new data frame with the season results

            # appends the data frame with season's results to data frame containing the data for all seasons
            blown_leads_all_seasons_data = blown_leads_all_seasons_data.append(blown_leads_single_season)

        # sorts the data by blown leads (descending) and then alphabetically (ascending)
        blown_leads_all_seasons_data = blown_leads_all_seasons_data.sort_values(by=['blown_leads', 'team_abbrv'], ascending=[False, True])

        return blown_leads_all_seasons_data

    def calculate_y_ticks(self, y_axis_max):
        """Calculates the correct number of ticks on the y-axis for a chart.

        Args:
            y_axis_max: the maximum value along the y-axis.

        Returns:
            A list of y_ticks, which will be consumed when generating the chart. For example:

            [0, 10, 20]

        """

        y_ticks = []

        # rounds the y_axis_max by 10, and then adds a tick mark for every 10th value
        for number in range(y_axis_max + 10):
            if number % 10 == 0:
                y_ticks.append(number)

        return y_ticks

    def convert_box_score_data_to_dataframe(self, box_score_data):
        """Converts each box score to a Box Score object, and then stores the Box Score object in a pandas dataframe.

        Args:
            box_score_data: the JSON object holding all the box score data collected by the get_box_score_data method.

        Returns:
            A pandas dataframe where the columns are fields from the Box Score object, and the rows are individual box scores. For example:

              team_abbrv                      team_name box_score_id season             home_team       home_team_innings_data                        home_team_other_data             away_team       away_team_innings_data                        away_team_other_data team_side  result  blown_leads
            0        ARI           Arizona Diamondbacks  ARI20120406   2012  Arizona Diamondbacks  [3, 0, 0, 0, 0, 2, 0, 0, X]   {'runs': '5', 'hits': '7', 'errors': '0'}  San Francisco Giants  [0, 0, 0, 0, 2, 1, 0, 0, 1]  {'runs': '4', 'hits': '11', 'errors': '3'}      home    True            0
            0        ARI           Arizona Diamondbacks  ARI20120407   2012  Arizona Diamondbacks  [2, 2, 0, 0, 1, 0, 0, 0, X]  {'runs': '5', 'hits': '10', 'errors': '0'}  San Francisco Giants  [0, 0, 0, 2, 0, 0, 2, 0, 0]   {'runs': '4', 'hits': '6', 'errors': '0'}      home    True            0
        """

        box_score_data_frame = pd.DataFrame()  # pandas data frame which will store all box score data

        # iterates through each season's box scores for each team
        for team in box_score_data:
            for season in box_score_data[team]:
                for box_score_id in box_score_data[team][season]:  # iterates through each key (box score id) in the box score data
                    box_score_raw_data = box_score_data[team][season][box_score_id]  # retrieves the raw box score data
                    box_score = BoxScore(box_score_raw_data, box_score_id, season, team)  # converts the raw box score data to a Box Score Object

                    # creates a temporary data frame where the column names are instance variables from the box score object, and the data is the values from the variables
                    columns = list(box_score.__dict__.keys())
                    values = list(box_score.__dict__.values())
                    temp_data_frame = pd.DataFrame([values], columns=columns)

                    box_score_data_frame = box_score_data_frame.append(temp_data_frame)  # adds the box score as a new row of data to the box score data frame

        return box_score_data_frame

    def create_blown_leads_per_season_data_frame(self, box_score_data_frame, seasons, team_abbrvs):
        """Collects the number of blown leads per team for each season.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            seasons: a list the number of seasons in the study
            team_abbrvs: the list of team abbreviations in the box score data frame, as calculated in the calculate_team_abbrvs method

        Returns:
            Returns a pandas dataframe where the indexes are team names, and the columns are blown lead totals for each season. For example:

                        Blown Leads 2012  Blown Leads 2013
            ARI               0.0               0.0
            ATL               0.0               0.0
            BAL               0.0               1.0
        """

        blown_leads_per_season_data = pd.DataFrame(index=team_abbrvs)  # the data frame that will store the blown leads data for each season

        for season in seasons:
            blown_leads_single_season_data = box_score_data_frame.where(box_score_data_frame['season'] == season).dropna()  # isolates data for the specific season

            # collects blown leads for each team in the season
            aggregation_function = {'blown_leads': 'sum'}
            blown_leads_single_season_data = blown_leads_single_season_data.groupby('team_abbrv').aggregate(aggregation_function)  # creates a new data frame containing the season data

            blown_leads_single_season_data = blown_leads_single_season_data.rename(columns={'blown_leads': f'Blown Leads {season}'})  # renames the blown leads column to include the season number

            blown_leads_per_season_data = blown_leads_per_season_data.merge(blown_leads_single_season_data, left_index=True, right_index=True)  # appends the season data frame to the data frame for all seasons

        return blown_leads_per_season_data

    def create_max_blown_leads_per_season_data_frame(self, box_score_data_frame, max_blown_leads_per_season, seasons):
        """Finds the names of the teams who blew the most leads for each season.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            max_blown_leads_per_season: the largest number of leads any team blew for each team, as calcuated in calculate_max_blown_leads_per_season
            seasons: a list the number of seasons in the study

        Returns:
            Returns a pandas dataframe containing the name of the team(s) that blew the most leads for each season, the season, and the number of leads
            they blew. For example:

                            blown_leads
            team_abbrv season
            CLE        2012            1.0
            TBR        2012            1.0
            BAL        2013            1.0
            CIN        2013            1.0
        """

        max_blown_leads_all_seasons_data_frame = pd.DataFrame()

        for season in seasons:
            # collects data for the season
            season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)

            # calculates the number of blown leads for each team for the season
            aggregation_function = {'blown_leads': 'sum'}
            season_data_frame = season_data_frame.groupby(['team_abbrv', 'season']).aggregate(aggregation_function)

            # retrieves the maximum number of blown leads for the season
            max_blown_leads_season = max_blown_leads_per_season[season]

            # creates a dataframe with the information for the team(s) who blew the most leads for the season
            max_blown_leads_data = season_data_frame.where(season_data_frame['blown_leads'] == max_blown_leads_season).dropna()

            # appends the season dataframe to the dataframe for all seasons
            max_blown_leads_all_seasons_data_frame = max_blown_leads_all_seasons_data_frame.append(max_blown_leads_data)

        return max_blown_leads_all_seasons_data_frame

    def create_max_blown_leads_tota_data_frame(self, box_score_data_frame, max_blown_leads_total):
        """Finds the name of the team(s) who blew the most leads over the study period.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            max_blown_leads_total: the largest number of leads any team blew over the study period, as calcuated in calculate_max_blown_leads_total

        Returns:
            Returns a pandas dataframe containing the name of the team(s) that blew the most leads over the study period. For example:

                        blown_leads
            team_abbrv
            STL                 2.0
        """

        # calculates the number of leads each team blew
        aggregation_function = {'blown_leads': 'sum'}
        max_blown_leads_total_data_frame = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)

        # finds the name of the team who blew the most leads
        max_blown_leads_total_data_frame = max_blown_leads_total_data_frame.where(max_blown_leads_total_data_frame['blown_leads'] == max_blown_leads_total).dropna()

        return max_blown_leads_total_data_frame

    def create_min_blown_leads_per_season_data_frame(self, box_score_data_frame, min_blown_leads_per_season, seasons):
        """Finds the names of the teams who blew the fewest leads for each season.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            min_blown_leads_per_season: the smallest number of leads any team blew for each team, as calcuated in calculate_min_blown_leads_per_season
            seasons: a list the number of seasons in the study

        Returns:
            Returns a pandas dataframe containing the name of the team(s) that blew the fewest leads for each season, the season, and the number of leads
            they blew. For example:

                                blown_leads
            team_abbrv season
            ARI        2012            0.0
            ATL        2012            0.0
            ARI        2013            0.0
            ATL        2013            0.0
        """

        min_blown_leads_all_seasons_data_frame = pd.DataFrame()

        for season in seasons:
            # collects data for the season
            season_data_frame = box_score_data_frame.where(box_score_data_frame['season'] == season)

            # calculates the number of blown leads for each team for the season
            aggregation_function = {'blown_leads': 'sum'}
            season_data_frame = season_data_frame.groupby(['team_abbrv', 'season']).aggregate(aggregation_function)

            # retrieves the minimum number of blown leads for the season
            min_blown_leads_season = min_blown_leads_per_season[season]

            # creates a dataframe with the information for the team(s) who blew the fewest leads for the season
            min_blown_leads_data = season_data_frame.where(season_data_frame['blown_leads'] == min_blown_leads_season).dropna()

            # appends the season dataframe to the dataframe for all seasons
            min_blown_leads_all_seasons_data_frame = min_blown_leads_all_seasons_data_frame.append(min_blown_leads_data)

        return min_blown_leads_all_seasons_data_frame

    def create_min_blown_leads_tota_data_frame(self, box_score_data_frame, min_blown_leads_total):
        """Finds the name of the team(s) who blew the fewest leads over the study period.

        Args:
            box_score_data_frame: the pandas dataframe holding every box score for study period, created in the convert_box_score_data_to_dataframe method
            min_blown_leads_total: the smallest number of leads any team blew over the study period, as calcuated in calculate_min_blown_leads_total

        Returns:
            Returns a pandas dataframe containing the name of the team(s) that blew the fewest leads over the study period. For example:

                        blown_leads
            team_abbrv
            ARI                 0.0
            ATL                 0.0
            BOS                 0.0
        """

        # calculates the number of leads each team blew
        aggregation_function = {'blown_leads': 'sum'}
        min_blown_leads_total_data_frame = box_score_data_frame.groupby('team_abbrv').aggregate(aggregation_function)

        # finds the name of the team who blew the fewest leads
        min_blown_leads_total_data_frame = min_blown_leads_total_data_frame.where(min_blown_leads_total_data_frame['blown_leads'] == min_blown_leads_total).dropna()

        return min_blown_leads_total_data_frame

    def get_box_score_data(self):
        """Reads the box score data from a JSON file, stores it in a nested JSON object, and returns the object."""

        with open(self.box_score_data_uri, 'r') as f:
            box_score_data = json.load(f)
            return box_score_data

    def plot_most_blown_leads_per_team_season_bar_chart(self, blown_leads_per_team_season_data_frame, seasons):
        """Creates a bar chart of the top 10 most blown leads for a team in a season, across the study period.

        Args:
            blown_leads_per_team_season_data_frame: the dataframe containing the number of blown leads for each team in a season, across the study period
            seasons: a list the number of seasons in the study

        Returns:
            Technically nothing, but it creates a png file with a bar chart of the top 10 most blown leads for a team in a season
        """

        # collects the top 10 most blown leads for a team in a season
        worst_blown_lead_seasons_data = blown_leads_per_team_season_data_frame.iloc[0:10]

        worst_blown_lead_seasons_plot = worst_blown_lead_seasons_data.plot(kind='bar')  # creates the plot object

        # configures the chart borders
        worst_blown_lead_seasons_plot.spines['right'].set_visible(False)
        worst_blown_lead_seasons_plot.spines['top'].set_visible(False)
        worst_blown_lead_seasons_plot.spines['left'].set_edgecolor('0.5')
        worst_blown_lead_seasons_plot.spines['left'].set_linewidth(1)
        worst_blown_lead_seasons_plot.spines['bottom'].set_edgecolor('0.5')
        worst_blown_lead_seasons_plot.spines['bottom'].set_linewidth(1)

        # configures the chart title, axis labels, axis ticks, grid, and spacing
        plt.title(f'Most Blown Leads\nin a Season: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
        plt.xlabel('Teams', labelpad=10, fontsize=12)
        plt.ylabel('Blown\nLeads', rotation=0, labelpad=40, fontsize=12)
        y_ticks = self.calculate_y_ticks(int(worst_blown_lead_seasons_data['blown_leads'].max()))
        plt.yticks(y_ticks, fontsize=8)
        plt.xticks(fontsize=8, rotation=45)
        plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
        plt.subplots_adjust(right=0.5)
        plt.tight_layout()

        # outputs the plot
        plt.savefig('results/most_blown_leads_in_a_season_bar.png')

    def plot_per_season_blown_leads_box_plot(self, blown_leads_per_season_data_frame, seasons):
        """Creates a box plot of the number of blown leads per team for each season.

        Args:
            blown_leads_per_season_data_frame: the data frame containing the number of blown leads per team for each season, as created in the create_blown_leads_per_season_data_frame method
            seasons: a list the number of seasons in the study

        Returns:
            Technically nothing, but it creates a png file with a box plot of the number of blown leads per team for each season
        """

        blown_leads_per_season_data_plot = blown_leads_per_season_data_frame.plot(kind='box')  # creates the plot object

        # configures the chart borders
        blown_leads_per_season_data_plot.spines['right'].set_visible(False)
        blown_leads_per_season_data_plot.spines['top'].set_visible(False)
        blown_leads_per_season_data_plot.spines['left'].set_edgecolor('0.5')
        blown_leads_per_season_data_plot.spines['left'].set_linewidth(1)
        blown_leads_per_season_data_plot.spines['bottom'].set_edgecolor('0.5')
        blown_leads_per_season_data_plot.spines['bottom'].set_linewidth(1)

        # configures the chart title, axis labels, axis ticks, grid, and spacing
        plt.title(f'Total Blown Leads\nfor each Season: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
        plt.xlabel('Seasons', labelpad=10, fontsize=12)
        blown_leads_per_season_data_plot.set_xticklabels(seasons)
        plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
        max_blown_leads_per_season_list = []
        for season in seasons:
            max_blown_leads_per_season_list.append(blown_leads_per_season_data_frame[f'Blown Leads {season}'].max())
        max_blown_leads_per_season = int(max(max_blown_leads_per_season_list))
        y_ticks = self.calculate_y_ticks(max_blown_leads_per_season)
        plt.yticks(y_ticks, fontsize=8)
        plt.xticks(fontsize=8)
        plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
        plt.subplots_adjust(right=0.5)
        plt.tight_layout()

        # outputs the plot
        plt.savefig('results/blown_leads_per_season_box_plot.png')

    def plot_stl_blown_leads_box_plot(self, blown_leads_stl_data_frame, seasons):
        """Creates a box plot of the blown leads for the St. Louis Cardinals for each season.

        Args:
            blown_leads_stl_data_frame: the data frame containing the number of blown leads per from each season for the St. Louis Cardinals
            seasons: a list the number of seasons in the study

        Returns:
            Technically nothing, but it creates a png file with a box plot of the blown leads for the St. Louis Cardinals for each season
        """

        stl_blown_leads_data_plot = blown_leads_stl_data_frame.plot(kind='box')  # creates the plot object

        # configures the chart borders
        stl_blown_leads_data_plot.spines['right'].set_visible(False)
        stl_blown_leads_data_plot.spines['top'].set_visible(False)
        stl_blown_leads_data_plot.spines['left'].set_edgecolor('0.5')
        stl_blown_leads_data_plot.spines['left'].set_linewidth(1)
        stl_blown_leads_data_plot.spines['bottom'].set_edgecolor('0.5')
        stl_blown_leads_data_plot.spines['bottom'].set_linewidth(1)

        # configures the chart title, axis labels, axis ticks, grid, and spacing
        plt.title(f'Total Blown Leads for the St. Louis Cardinals: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
        plt.xlabel('STL', labelpad=10, fontsize=12)
        stl_blown_leads_data_plot.set_xticklabels('')
        plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
        stl_max_blown_leads = int(blown_leads_stl_data_frame['STL'].max())
        y_ticks = self.calculate_y_ticks(stl_max_blown_leads)
        plt.yticks(y_ticks, fontsize=8)
        plt.xticks(fontsize=8)
        plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')

        # outputs the plot
        plt.savefig('results/stl_blown_leads.png', bbox_inches='tight')

    def plot_total_blown_leads_bar_chart(self, blown_leads_total_data_frame, seasons):
        """Creates a bar chart of the total number of blown leads for each team.

        Args:
            blown_leads_total_data_frame: the dataframe containing the number of blown leads belonging to each team (producded in the calculate_total_blown_leads method)
            seasons: a list the number of seasons in the study

        Returns:
            Technically nothing, but it creates a png file with a bar chart of the total blown leads for each team
        """

        blown_leads_total_data_plot = blown_leads_total_data_frame.plot(kind='bar')  # creates the plot object

        # configures the chart borders
        blown_leads_total_data_plot.spines['right'].set_visible(False)
        blown_leads_total_data_plot.spines['top'].set_visible(False)
        blown_leads_total_data_plot.spines['left'].set_edgecolor('0.5')
        blown_leads_total_data_plot.spines['left'].set_linewidth(1)
        blown_leads_total_data_plot.spines['bottom'].set_edgecolor('0.5')
        blown_leads_total_data_plot.spines['bottom'].set_linewidth(1)

        # configures the chart title, axis labels, axis ticks, grid, and spacing
        plt.title(f'Total Blown Leads: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
        plt.xlabel('Teams', labelpad=10, fontsize=12)
        plt.ylabel('Blown\nLeads', rotation=0, labelpad=40, fontsize=12)
        y_ticks = self.calculate_y_ticks(blown_leads_total_data_frame['blown_leads'].max())
        plt.yticks(y_ticks, fontsize=8)
        plt.xticks(fontsize=8)
        plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
        plt.subplots_adjust(right=0.5)
        plt.tight_layout()

        # outputs the plot
        plt.savefig('results/blown_leads_total_data_bar_chart.png')

    def plot_total_blown_leads_box_plot(self, blown_leads_total_data_frame, seasons):
        """Creates a box plot of the total number of blown leads per team.

        Args:
            blown_leads_total_data_frame: the dataframe containing the number of blown leads belonging to each team (producded in the calculate_total_blown_leads method)
            seasons: a list the number of seasons in the study

        Returns:
            Technically nothing, but it creates a png file with a box plot of the total blown leads per team
        """

        blown_leads_total_data_plot = blown_leads_total_data_frame.plot(kind='box')  # creates the plot object

        # configures the chart borders
        blown_leads_total_data_plot.spines['right'].set_visible(False)
        blown_leads_total_data_plot.spines['top'].set_visible(False)
        blown_leads_total_data_plot.spines['left'].set_edgecolor('0.5')
        blown_leads_total_data_plot.spines['left'].set_linewidth(1)
        blown_leads_total_data_plot.spines['bottom'].set_edgecolor('0.5')
        blown_leads_total_data_plot.spines['bottom'].set_linewidth(1)

        # configures the chart title, axis labels, axis ticks, grid, and spacing
        plt.title(f'Total Blown Leads: {seasons[0]}-{seasons[-1]}', y=1.10, fontsize=16)
        plt.xlabel('All Teams', labelpad=10, fontsize=12)
        blown_leads_total_data_plot.set_xticklabels('')  # hides the x tick label
        plt.ylabel('Blown\nLeads', rotation=0, labelpad=30, fontsize=12)
        y_ticks = self.calculate_y_ticks(blown_leads_total_data_frame['blown_leads'].max())
        plt.yticks(y_ticks, fontsize=8)
        plt.xticks(fontsize=8)
        plt.grid(True, color='0.75', linestyle='--', which='both', axis='y')
        plt.subplots_adjust(right=0.5)
        plt.tight_layout()

        # outputs the plot
        plt.savefig('results/blown_leads_total_data_box_plot.png')

    def output_results(self, box_score_data_frame, max_blown_leads_total, min_blown_leads_total, max_blown_leads_total_data_frame,
                       min_blown_leads_total_data_frame, blown_leads_all_seasons_dict, max_blown_leads_per_season_data_frame,
                       min_blown_leads_per_season_data_frame, blown_leads_per_season_dict, blown_leads_stl_stats_dict,
                       stl_blown_lead_losses_stats_dict):
        """Writes a text file with the results of the data analysis.

        Args:
            A collection of the statistics and data generated by the box_score_data_analysis.py program

        Returns:
            Technically nothing, but it creates a text file with the data analysis results.
        """

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
            f.write(str(max_blown_leads_per_season_data_frame) + '\n\n')
            f.write('Data for the team(s) with the fewest blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
            f.write(str(min_blown_leads_per_season_data_frame) + '\n\n')
            f.write('Data on the mean, mode, and median blown leads for each season from ' + seasons[0] + '-' + seasons[-1] + ':\n')
            for season in seasons:
                f.write(season + ' Data:\n')
                f.write('\tMean: ' + str(blown_leads_per_season_dict[season]['mean']) + '\n')
                f.write('\tMode: ' + str(blown_leads_per_season_dict[season]['mode']) + '\n')
                f.write('\tMedian: ' + str(blown_leads_per_season_dict[season]['median']) + '\n\n')
            f.write('St. Louis Cardinals Blown Leads Data:\n')
            f.write('\tAverage number of blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(blown_leads_stl_stats_dict['mean']) + '\n')
            f.write('\tSeason with the most blown leads: ' + str(blown_leads_stl_stats_dict['maximum']) + '\n')
            f.write('\tSeason with the fewest blown leads: ' + str(blown_leads_stl_stats_dict['minimum']) + '\n\n')
            f.write('Data on the mean, mode, and median blown leads for all seasons ' + seasons[0] + '-' + seasons[-1] + ':\n')
            f.write('\tMean: ' + str(blown_leads_stl_stats_dict['mean']) + '\n')
            f.write('\tMode: ' + str(blown_leads_stl_stats_dict['mode']) + '\n')
            f.write('\tMedian: ' + str(blown_leads_stl_stats_dict['median']) + '\n\n')
            f.write('Data on games where the St. Louis Cardinals blew at least one lead and lost:\n')
            f.write('\tTotal number of "blown lead losses" for the St. Louis Cardinals from seasons ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_lead_losses_stats_dict['total']) + '\n')
            f.write('\tAverage number of "blown lead losses" for the St. Louis Cardinals per season from ' + seasons[0] + '-' + seasons[-1] + ': ' + str(stl_blown_lead_losses_stats_dict['mean']) + '\n')
            f.write('\tNumber of "blown lead losses" from ' + seasons[0] + '-' + seasons[-1] + ':\n')
            for season in seasons:
                f.write('\t\t' + season + ' Blown Lead Losses: ' + str(stl_blown_lead_losses_stats_dict['seasons'][season]) + '\n')
