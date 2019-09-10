import json


class MlbTeamConfigUtils:
    def __init__(self, mlb_team_config_uri):
        self.mlb_team_config_uri = mlb_team_config_uri

    def get_config_data(self):
        with open(self.mlb_team_config_uri, 'r') as config_file:
            team_config_data = json.load(config_file)
        return team_config_data

    def get_team_abbrvs(self):
        with open(self.mlb_team_config_uri, 'r') as config_file:
            team_config_data = json.load(config_file)
            team_abbrvs = []
            for team_abbrv in team_config_data['team_abbreviations']:
                team_abbrvs.append(team_abbrv)
        return team_abbrvs
