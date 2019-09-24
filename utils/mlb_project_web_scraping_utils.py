from bs4 import BeautifulSoup
import requests
import json
import logging
import sys
logging.basicConfig(format='%(asctime)s - %(filename)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s',
                    level=logging.INFO)


class MlbWebScrapingUtils:
    """A collection of utility methods that web scrape data from baseball reference.

    Attributes:
        self.team_abbrvs: the list of team abbreviations.
        self.seasons: the list of seasons to web scrape data for.
        self.base_url: the base part of the url to the baseball reference season home pages (e.g., the home page for Arizona's 2012 season).
        self.logger: python logging object.
    """

    def __init__(self, team_abbrvs, seasons, base_url):
        """Inititalizes MlbWebScrapingUtils class with self.team_abbrvs, self.seasons, self.base_url, self.logger"""

        self.team_abbrvs = team_abbrvs
        self.seasons = seasons
        self.base_url = base_url
        self.logger = logging.getLogger()

    def url_generator(self):
        """Generates the url for the baseball reference season home page (which contains the urls for every box score for a season) for all teams.

        Args:
            None technically, but it calls two instance variables:
            self.team_abbrvs: the list of team abbreviations.
            self.base_url: the base part of the url to the baseball reference season home pages.

        Returns:
            A dictionary mapping each team to a list of 'season dictionaries' where the keys are seasons, and the values are the corresponding
            urls to the baseball reference season home page. For example:

            {
            'ARI': [
                {2012: 'https://www.baseball-reference.com/teams/ARI/2012-schedule-scores.shtml'},
                {2013: 'https://www.baseball-reference.com/teams/ARI/2013-schedule-scores.shtml'}
            ],
            'ATL': ...
            }
        """

        home_page_urls_dict = {}

        for team in self.team_abbrvs:
            home_page_urls_dict[team] = []  # declares the list that will hold all the team's 'season dictionaries'

            for season in self.seasons:
                season_home_page_url_dict = {}  # creates an individual 'season dictionary'
                season_home_page_url_dict[season] = f'{self.base_url}/{team}/{season}-schedule-scores.shtml'  # creates the full season home page url, and stores it in the 'season dictionary'
                home_page_urls_dict[team].append(season_home_page_url_dict)  # stores the 'season dictionary' in the team's dictionary

        return home_page_urls_dict

    def collect_box_scores(self, box_score_urls):
        """A handler method that manages the collection of the box score data for each team for all seasons in self.seasons.

        Args:
            box_score_urls: the list of box score urls (for each team, for each season) collected in the collect_box_score_urls method.

        Returns:
            A nested JSON obejct which maps each team to a 'team dictionary'. The keys for each team dictionary are season numbers (e.g., 2012),
            and the values are box score like JSON objects. A box score like object is a dictionary where the key is a box score id, and the value
            is the box score data. For example:

            {
            "ARI": {
                "2012": {
                    "ARI20120406": {
                        "home_team": {
                            "team_name": "Arizona Diamondbacks",
                            "inning_data": {
                                "1": "3", "2": "0", "3": "0", "4": "0", "5": "0", "6": "2", "7": "0", "8": "0", "9": "X"
                                },
                            "other_box_score_data": {
                                "runs": "5", "hits": "7", "errors": "0"
                            }
                        },
                        "away_team": {
                            "team_name": "San Francisco Giants",
                            "inning_data": {
                                "1": "0", "2": "0", "3": "0", "4": "0", "5": "2", "6": "1", "7": "0", "8": "0", "9": "1"
                            },
                            "other_box_score_data": {
                                "runs": "4", "hits": "11", "errors": "3"
                            }
                        }
                    },
                    "ARI20120407": {
                        ...
                    }
                },
                "2013": {
                    ...
                    }
                },
            "ATL": ...
            }
        """

        box_scores_data_object = {}

        for team in box_score_urls:  # iterates through each key (team abbreviations) in the box_score_urls
            teams_box_scores = {}

            # iterates through each team's 'season dictionaries' containing the box score urls for each season
            for team_urls_dict in box_score_urls[team]:

                for season in team_urls_dict:
                    season_box_scores_dict = {}
                    index = 0  # Delete

                    for box_score_url in team_urls_dict[season]:
                        self.logger.info(f'Collecting data for {team} {season} {box_score_url}')
                        if index < 2:  # Delete
                            box_score_id = self.__generate_box_score_id(box_score_url, team)  # a unique identifier for a box score
                            season_box_scores_dict[box_score_id] = self.__get_box_score(box_score_url)  # collects the data from each box score, and stores it with the box score id in the season_box_scores_dict
                        index += 1  # Delete

                    teams_box_scores[season] = season_box_scores_dict

            box_scores_data_object[team] = teams_box_scores

        return box_scores_data_object

    def collect_box_score_urls(self, home_page_urls_dict, box_score_base_url):
        """A handler method that manages the collection of the urls for the box scores for each team for all seasons in self.seasons.

        Args:
            home_page_urls_dict: the dictionary object created in the url_generator method.
            box_score_base_url: the base string that all box score urls share in common (e.g., https://www.baseball-reference.com/)

        Returns:
            A dictionary mapping each team to a list of 'season dictionaries' where the keys are seasons, and the values are lists where
            each element is a url to a box score from that season. For example:

            {
                "ARI": [
                    {"2012": [
                        "https://www.baseball-reference.com//boxes/ARI/ARI201204060.shtml",
                        "https://www.baseball-reference.com//boxes/ARI/ARI201204070.shtml",
                        "https://www.baseball-reference.com//boxes/ARI/ARI201204080.shtml",
                        ]
                    },
                    {"2013": [
                        "https://www.baseball-reference.com//boxes/ARI/ARI201304010.shtml",
                        "https://www.baseball-reference.com//boxes/ARI/ARI201304020.shtml",
                        "https://www.baseball-reference.com//boxes/ARI/ARI201304030.shtml"
                        ]
                    }
                ],
                "ATL": ...
            }
        """

        box_score_urls_dict = {}

        for team in home_page_urls_dict:  # iterates through each key (team abbreviations) in the home_page_urls_dict
            team_box_scores = []

            for season_home_page_url_dict in home_page_urls_dict[team]:  # iterates through each 'season dictionary' for a team
                season_box_scores_urls_dict = {}
                season = [season for season in season_home_page_url_dict][0]  # retrieves the season number from the 'season dictionary' as a string
                self.logger.info(f'Collecting box score urls for {season} {team}')
                season_home_page_url = season_home_page_url_dict[season]  # retrieves the season home page url
                season_box_scores_urls_dict[season] = self.__get_box_score_urls(season_home_page_url, box_score_base_url)  # collects all the team's box score urls for a season
                team_box_scores.append(season_box_scores_urls_dict)

            box_score_urls_dict[team] = team_box_scores

        return box_score_urls_dict

    def __generate_box_score_id(self, box_score_url, team):
        """Generates a unique identifier for a box score.

        Args:
            box_score_url: the baseball reference url for the box score.
            team: team abbreviation.

        Returns:
            A unique identifier comprised of the name and box score id. For example:

            "ARI20120406"
        """

        # isolates the box score id and then adds the team abbreviation to it
        box_score_id = box_score_url.split('/')
        box_score_id = box_score_id[-1]
        box_score_id = box_score_id.split('.')
        box_score_id = team + box_score_id[0][3:-1]

        return box_score_id

    def __get_box_score(self, box_score_url):
        response_object = requests.get(box_score_url)
        if response_object.status_code == 200:
            box_score = {}
            response_text = response_object.text
            soup_object = BeautifulSoup(response_text, 'lxml')
            box_score_container = soup_object.find('table', {'class': 'linescore nohover stats_table no_freeze'})
            box_score_element = box_score_container.tbody
            box_score_rows = box_score_element.find_all('tr')
            # away team
            away_team_element = box_score_rows[0]
            away_team_name = away_team_element.find_all('td')[1].text
            away_team_inning_elements = away_team_element.find_all('td')[2:-3]
            away_team_inning_data = {}
            inning = 1
            # collect away team inning data for all innings in a game
            for inning_element in away_team_inning_elements:
                away_team_inning_data[str(inning)] = inning_element.text
                inning += 1
            # collect away team other box score data (runs, hits, errors)
            away_team_other_box_score_data = {}
            index = 0
            for data_element in away_team_element.find_all('td')[-3:]:
                if index == 0:
                    away_team_other_box_score_data['runs'] = data_element.text
                elif index == 1:
                    away_team_other_box_score_data['hits'] = data_element.text
                elif index == 2:
                    away_team_other_box_score_data['errors'] = data_element.text
                index += 1
            # home team
            home_team_element = box_score_rows[1]
            home_team_name = home_team_element.find_all('td')[1].text
            home_team_inning_elements = home_team_element.find_all('td')[2:-3]
            home_team_inning_data = {}
            inning = 1
            # collect home team inning data for all innings in a game
            for inning_element in home_team_inning_elements:
                home_team_inning_data[str(inning)] = inning_element.text
                inning += 1
            # collect home team other box score data (runs, hits, errors)
            home_team_other_data_elements = home_team_element.find_all('td')[-3:]
            home_team_other_box_score_data = {}
            index = 0
            for data_element in home_team_other_data_elements:
                if index == 0:
                    home_team_other_box_score_data['runs'] = data_element.text
                elif index == 1:
                    home_team_other_box_score_data['hits'] = data_element.text
                elif index == 2:
                    home_team_other_box_score_data['errors'] = data_element.text
                index += 1
            # organize data into box score
            home_team_box_score = {}
            home_team_box_score['team_name'] = home_team_name
            home_team_box_score['inning_data'] = home_team_inning_data
            home_team_box_score['other_box_score_data'] = home_team_other_box_score_data
            away_team_box_score = {}
            away_team_box_score['team_name'] = away_team_name
            away_team_box_score['inning_data'] = away_team_inning_data
            away_team_box_score['other_box_score_data'] = away_team_other_box_score_data
            box_score['home_team'] = home_team_box_score
            box_score['away_team'] = away_team_box_score
        return box_score

    def __get_box_score_urls(self, season_home_page_url, box_score_base_url):
        """Web scrapes a team's baseball reference season home page, to collect the urls for the box scores for an entire season.

        Args:
            season_home_page_url: the url to the team's baseball reference season home page
            box_score_base_url: the base string that all box score urls share in common (e.g., https://www.baseball-reference.com/)

        Returns:
            A list of urls for all the team's box scores for a season. For example:

            ['https://www.baseball-reference.com//boxes/ARI/ARI201304010.shtml',
            'https://www.baseball-reference.com//boxes/ARI/ARI201304020.shtml',
            'https://www.baseball-reference.com//boxes/ARI/ARI201304030.shtml']

        Exceptions:
            Catches all AttributeErrors which are encountered while trying to web scrape the table in the season home page that
            stores the box score urls. Not every row in that table has a box score url, in which case searching for it results in
            an AttributeError.
        """

        box_score_urls = []

        # retrieves the html from a season home page via a get request
        response_object = requests.get(season_home_page_url)
        response_text = response_object.text

        if response_object.status_code == 200:  # if the get request is successful

            # searches the season home page html for the table (i.e., schedule table) where box score urls are stored
            soup_object = BeautifulSoup(response_text, 'lxml')
            schedule_table_object = soup_object.find('table', id='team_schedule')
            schedule_table_rows_object = schedule_table_object.tbody
            schedule_table_rows = schedule_table_rows_object.find_all('tr')

            for row in schedule_table_rows:

                # if the row in the schedule table has a box score url in it, collects the box score url, and appends it to the list of box score urls
                try:
                    boxscore_element = row.find('td', {'data-stat': 'boxscore'})
                    box_score_url_fragment = boxscore_element.a['href']
                    box_score_url = box_score_base_url + box_score_url_fragment
                    box_score_urls.append(box_score_url)

                # if the row in the table does not have a box score url (and can therefore safely be ingored), the program notes the ocurrence and moves on
                except AttributeError as e:
                    self.logger.debug(f'Non-boxscore row found {e}')

            return box_score_urls

        else:  # if the get request is unsuccessful
            self.logger.error(f'Unexected error collecting box score urls. Response object returned with non-200 status code: {response_object.status_code}')
            sys.exit()  # terminates the program

    def output_box_score_data(self, box_scores, output_file_name):
        """Writes the box score data to a JSON file."""
        with open(output_file_name, 'w') as f:
            json.dump(box_scores, f)
