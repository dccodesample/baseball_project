import json
import pandas as pd
from src.BoxScore import BoxScore


class BoxScoreDataAnalysisUtils:
    def __init__(self, box_score_data_uri):
        self.box_score_data_uri = box_score_data_uri

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

        box_score_data_frame = pd.DataFrame()  # dataframe which will store all box score data

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

    def get_box_score_data(self):
        """Reads the box score data from a JSON file, stores it in a nested JSON object, and returns the object."""

        with open('data/box_score_data.json', 'r') as f:
            box_score_data = json.load(f)
            return box_score_data
