import json


class MlbTeamConfigUtils:
    """Collects data from a mlb team config data file.

    Attributes:
        self.mlb_team_config_uri: the uri to the config data file.
    """

    def __init__(self, mlb_team_config_uri):
        """Initializes the MlbTeamConfigUtils class with self.mlb_team_config_uri."""
        self.mlb_team_config_uri = mlb_team_config_uri

    def get_config_data(self):
        """Opens the config data file and returns all the data in a JSON object."""

        with open(self.mlb_team_config_uri, 'r') as config_file:
            team_config_data = json.load(config_file)

        return team_config_data

    def get_team_abbrvs(self):
        """Opens the config data file and retrieves the abbreviation for each team.

        Args:
            None technically, but it calls self.mlb_team_config_uri: the uri to the config data file.

        Returns:
            A list of all team name abbreviations, e.g.:

            ['ARI', 'ATL', 'BAL', ... 'WSN']
        """

        with open(self.mlb_team_config_uri, 'r') as config_file:  # opens the config file
            team_config_data = json.load(config_file)  # loads the data into a json object
            team_abbrvs = []

            for team_abbrv in team_config_data['team_abbreviations']:  # iterates through each value in the 'team_abbreviations' key
                team_abbrvs.append(team_abbrv)

        return team_abbrvs
