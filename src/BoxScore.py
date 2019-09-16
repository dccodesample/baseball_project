import json
from utils.mlb_project_config_utils import MlbTeamConfigUtils


class BoxScore:
    def __init__(self, box_score_data, box_score_id, season, team_abbrv):
        self.team_abbrv = team_abbrv
        self.team_name = self.get_team_name()
        self.box_score_id = box_score_id
        self.season = season

        self.home_team = box_score_data['home_team']['team_name']
        self.home_team_innings_data = list(dict(box_score_data['home_team']['inning_data']).values())
        self.home_team_other_data = box_score_data['home_team']['other_box_score_data']

        self.away_team = box_score_data['away_team']['team_name']
        self.away_team_innings_data = list(dict(box_score_data['away_team']['inning_data']).values())
        self.away_team_other_data = box_score_data['away_team']['other_box_score_data']

        self.team_side = self.get_team_side()
        self.result = self.get_result()
        self.blown_leads = self.calculate_blown_leads()

    def calculate_blown_leads(self):
        """Checks to see if the team had a run of 3 runs or greater and lost it"""
        number_of_innings = len(self.away_team_innings_data)
        # compline box score inning data into one list
        inning_data = []
        for inning in range(number_of_innings):
            inning_data.append(self.away_team_innings_data[inning])
            inning_data.append(self.home_team_innings_data[inning])
        away_team_run_differentials = []
        home_team_run_differentials = []
        for index in range(len(inning_data) + 1):
            try:
                if index % 2 == 0:
                    if index == 0:
                        inning_away_team_run_differential = int(inning_data[index]) - 0
                        away_team_run_differentials.append(inning_away_team_run_differential)
                    else:
                        inning_away_team_run_differential = int(inning_data[index]) - int(inning_data[index - 1])
                        away_team_run_differentials.append(inning_away_team_run_differential)

                else:
                    if inning_data[index].isnumeric():
                        inning_home_team_run_differential = int(inning_data[index]) - int(inning_data[index - 1])
                        home_team_run_differentials.append(inning_home_team_run_differential)
                    else:
                        break
            except Exception as e:
                # checks that the away team did not blown a lead in the bottom of the 9th
                if inning_data[index - 1].isnumeric():
                    inning_away_team_run_differential = 0 - int(inning_data[index - 1])
                    away_team_run_differentials.append(inning_away_team_run_differential)
                print(e)
        away_team_run_differntial_running_total = 0
        lead = False
        away_team_blown_leads = 0
        for inning in away_team_run_differentials:
            away_team_run_differntial_running_total += inning
            if away_team_run_differntial_running_total >= 3:
                lead = True
            if lead is True and away_team_run_differntial_running_total <= 0:
                lead = False
                away_team_blown_leads += 1
        home_team_run_differntial_running_total = 0
        lead = False
        home_team_blown_leads = 0
        for inning in home_team_run_differentials:
            home_team_run_differntial_running_total += inning
            if home_team_run_differntial_running_total >= 3:
                lead = True
            if lead is True and home_team_run_differntial_running_total <= 0:
                lead = False
                home_team_blown_leads += 1
        blown_leads = {}
        blown_leads['away'] = away_team_blown_leads
        blown_leads['home'] = home_team_blown_leads
        return blown_leads[self.team_side]

    def __calculate_winner(self):
        home_team_score = int(self.home_team_other_data['runs'])
        away_team_score = int(self.away_team_other_data['runs'])
        return self.home_team if home_team_score > away_team_score else self.away_team

    def get_result(self):
        winner = self.__calculate_winner()
        return True if self.team_name == winner else False

    def get_team_name(self, mlb_config_data_path='config/mlb_config_data.json'):
        mlb_team_config_utils = MlbTeamConfigUtils(mlb_config_data_path)
        team_name_data = mlb_team_config_utils.get_config_data()['team_abbreviations']
        for team in team_name_data:
            if team == self.team_abbrv:
                return team_name_data[team]

    def get_team_side(self):
        if self.team_name == self.home_team:
            return 'home'
        else:
            return 'away'
