from utils.mlb_project_config_utils import MlbTeamConfigUtils
import logging
import sys
logging.basicConfig(format='%(asctime)s - %(filename)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()


class BoxScore:
    """
    A class representing 1) a box score, and 2) containing requisite information that will be needed to complete data analysis on blown leads.

    Attributes:

        self.team_abbrv: the abbreviation for the team the box score belongs to (e.g., ARI)
        self.team_name: the full name for the team
        self.box_score_id: the unique identifier for a box score
        self.season: the season number the box score belongs to (e.g., 2012)

        self.home_team: the full team name of the home team
        self.home_team_innings_data: the innings data for the home team (dictionary where keys are inning numbers, and values are the runs scored in the innings)
        self.home_team_other_data: the runs, hits, and errors data for the home team

        self.away_team: the full team name of the away team
        self.away_team_innings_data: the innings data for the away team (dictionary where keys are inning numbers, and values are the runs scored in the innings)
        self.away_team_other_data: the runs, hits, and errors data for the away team

        self.team_side: A string indicating which side (away or home) the team was
        self.result = A boolean indicating whether or not the team won (True is won, False if lost)
        self.blown_leads = The number of leads the team blew
    """

    def __init__(self, box_score_data, box_score_id, season, team_abbrv):
        """Initializes the BoxScore class with all its attributes.

        Args:
            box_score_data: an individual box score nested JSON object.
            box_score_id: the unique identifier for the box score.
            season: the season number for the box score (e.g., 2012).
            team_abbrv: the team abbreviation for the team the box score belongs to.
        """

        self.team_abbrv = team_abbrv
        self.team_name = self.get_team_name()
        self.box_score_id = box_score_id
        self.season = season

        self.home_team = box_score_data['home_team']['team_name']
        self.home_team_innings_data = list(dict(box_score_data['home_team']['inning_data']).values())  # for the home team, collects all the values (runs in an inning) from the box score
        self.home_team_other_data = box_score_data['home_team']['other_box_score_data']

        self.away_team = box_score_data['away_team']['team_name']
        self.away_team_innings_data = list(dict(box_score_data['away_team']['inning_data']).values())  # for the away team, collects all the values (runs in an inning) from the box score
        self.away_team_other_data = box_score_data['away_team']['other_box_score_data']

        self.team_side = self.get_team_side()
        self.result = self.get_result()
        self.blown_leads = self.calculate_blown_leads()

    def calculate_blown_leads(self):
        """Calculates how many times the team the box score belongs to had a lead of 3 runs or greater and lost it.

        Args:
            None technically, but the following instance variables are used:
            self.away_team_innings_data: a dictionary for the away team, where the keys are inning numbers, and the values are the runs scored in the corresponding inning
            self.home_team_innings_data: a dictionary for the home team, where the keys are inning numbers, and the values are the runs scored in the corresponding inning
            self.team_side: A string indicating which side the team the box score belongs to is on (home or away)

        Returns:
            The number of blown leads the team the box score belongs to blew in the game.

        Exceptions:
            While iterating through each sides data, catches any IndexErrors, because the method's logic requires it to iterate one element past the end of the inning_data list's length.
        """

        number_of_innings = len(self.away_team_innings_data)

        # Complines the box score inning data for both sides into a single list
        inning_data = []
        for inning in range(number_of_innings):
            inning_data.append(self.away_team_innings_data[inning])
            inning_data.append(self.home_team_innings_data[inning])

        # for each half-inning, calculates the difference between one side's score after they get done batting, and the other team's score after they were done batting.
        # iterates through the inning_data list, where each side's run total for their turn at bat alternates
        away_team_run_differentials = []
        home_team_run_differentials = []
        for index in range(len(inning_data) + 1):

            try:
                if index % 2 == 0:  # if the element belongs to the away team

                    if index == 0:  # if the element represents the first time the away team is at bat, compares to zero because the home team has not batted yet and therefore there is no run total for the previous half-inning
                        inning_away_team_run_differential = int(inning_data[index]) - 0
                        away_team_run_differentials.append(inning_away_team_run_differential)

                    else:  # for all other elements, compares the away team's run total from their turn at bat against the home team's run total from their previous turn at bat, and stores the difference
                        inning_away_team_run_differential = int(inning_data[index]) - int(inning_data[index - 1])
                        away_team_run_differentials.append(inning_away_team_run_differential)

                else:  # if the element belongs to the home team

                    # checks that the element value is not 'X' which happens if the home team has a lead after the top of the 9th inning, and therefore does not have to bat
                    # if it is not, compares the home team's run total from the turn at bat to the away team's run total from their previous time at bat, and stores the difference
                    if inning_data[index].isnumeric():
                        inning_home_team_run_differential = int(inning_data[index]) - int(inning_data[index - 1])
                        home_team_run_differentials.append(inning_home_team_run_differential)

                    else:
                        break

            except IndexError as e:

                # Checks that the away team did not blown a lead in the bottom of the last inning
                if inning_data[index - 1].isnumeric():
                    inning_away_team_run_differential = 0 - int(inning_data[index - 1])
                    away_team_run_differentials.append(inning_away_team_run_differential)

                logger.debug(f'Index Error: {e}')

        away_team_run_differntial_running_total = 0
        lead = False
        away_team_blown_leads = 0

        # calculates how many leads the away team blew
        # adds up the individual run differentials for each inning, to create a running total for run differential
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

        # calculates how many leads the home team blew
        # adds up the individual run differentials for each inning, to create a running total for run differential
        for inning in home_team_run_differentials:
            home_team_run_differntial_running_total += inning

            if home_team_run_differntial_running_total >= 3:
                lead = True

            if lead is True and home_team_run_differntial_running_total <= 0:
                lead = False
                home_team_blown_leads += 1

        # returns the number of leads that the team blew
        blown_leads = {}
        blown_leads['away'] = away_team_blown_leads
        blown_leads['home'] = home_team_blown_leads

        return blown_leads[self.team_side]

    def get_result(self):
        """Calculates which side won the game, and if that is the side of team the box score belongs to.

        Args:
            None technically, but the following instance variables are used:
            self.home_team: the full name of the home team
            self.away_team: the full name of the away team
            self.home_team_other_data: the runs, hits, and errors data for the home team
            self.away_team_other_data: the runs, hits, and errors data for the away team

        Returns:
            A boolean indicating whether or not the team the box score belongs to won the game. True is they won, False if they lost.
        """

        home_team_score = int(self.home_team_other_data['runs'])
        away_team_score = int(self.away_team_other_data['runs'])

        winner = self.home_team if home_team_score > away_team_score else self.away_team  # sets winner to the side whose run total is greatest

        return True if self.team_name == winner else False  # true if winner is equal to the team's name, else false

    def get_team_name(self, mlb_config_data_path='config/mlb_config_data.json'):
        """Finds the full name of the team the box score belongs to.

        Args:
            mlb_config_data_path: the uri of the mlb config data file, set as a default to 'config/mlb_config_data.json'
            Not technically an arg, but the following instance variable is used:
            self.team_abbrv: the abbreviation of the team the box score belongs to

        Returns:
            A string of the full name of the team the box score belongs to. For example, 'Arizona Diamondbacks'.
        """

        # opens the mlb config data file
        mlb_team_config_utils = MlbTeamConfigUtils(mlb_config_data_path)
        team_name_data = mlb_team_config_utils.get_config_data()['team_abbreviations']

        # searches for the team's abbreviation, and pulls the corresponding team name
        for team in team_name_data:
            if team == self.team_abbrv:
                return team_name_data[team]

        # terminates the program if it cannot find the team's full name
        logger.error('Could not find team abbreviation "{self.team_abbrv}" in the mlb config data file located here: {mlb_config_data_path}')
        sys.exit()

    def get_team_side(self):
        """Discovers which side the team the box score belongs to is on."""

        if self.team_name == self.home_team:
            return 'home'
        else:
            return 'away'
