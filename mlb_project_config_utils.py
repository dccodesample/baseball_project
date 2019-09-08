import json


class MlbTeamConfigUtils:
    def __init__(self, mlb_team_config_uri):
        self.mlb_team_config_uri = mlb_team_config_uri
    
    def get_team_abbrvs(self):
        with open(self.mlb_team_config_uri, 'r') as config_file:
            team_config_data = json.load(config_file)
            team_abbrvs = team_config_data['team_abbreviations']
        return team_abbrvs
