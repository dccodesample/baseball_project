from bs4 import BeautifulSoup
import requests
import json


class MlbWebScrapingUtils:
    def __init__(self, team_abbrvs, years, base_url):
        self.team_abbrvs = team_abbrvs
        self.years = years
        self.base_url = base_url

    def url_generator(self):
        home_page_urls = {}
        for team in self.team_abbrvs:
            home_page_urls[team] = []
            for year in self.years:
                season_home_page_url = {}
                season_home_page_url[year] = f'{self.base_url}/{team}/{year}-schedule-scores.shtml'
                home_page_urls[team].append(season_home_page_url)
        return home_page_urls

    def collect_box_scores(self, box_score_urls):
        box_scores = {}
        for team in box_score_urls:
            teams_box_scores = {}
            for team_urls_dict in box_score_urls[team]:
                for season in team_urls_dict:
                    season_box_scores = {}
                    # index = 0
                    for box_score_url in team_urls_dict[season]:
                        print(team, season, box_score_url)
                        # if index < 2:
                        box_score_id = self.__generate_box_score_id(box_score_url, team)
                        season_box_scores[box_score_id] = self.__get_box_score(box_score_url)
                        # index += 1
                    teams_box_scores[season] = season_box_scores
            box_scores[team] = teams_box_scores
        return box_scores

    def collect_box_score_urls(self, home_page_urls, box_score_base_url):
        box_score_urls = {}
        for team in home_page_urls:
            team_box_scores = []
            for season_home_page in home_page_urls[team]:
                season_box_scores = {}
                year = [year for year in season_home_page][0]
                print(team, year)
                season_home_page_url = season_home_page[year]
                season_box_scores[year] = self.__get_box_score_urls(season_home_page_url, box_score_base_url)
                team_box_scores.append(season_box_scores)
            box_score_urls[team] = team_box_scores
        return box_score_urls

    def __generate_box_score_id(self, box_score_url, team):
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
        box_score_urls = []
        response_object = requests.get(season_home_page_url)
        response_text = response_object.text
        if response_object.status_code == 200:
            soup_object = BeautifulSoup(response_text, 'lxml')
            schedule_table_object = soup_object.find('table', id='team_schedule')
            schedule_table_rows_object = schedule_table_object.tbody
            schedule_table_rows = schedule_table_rows_object.find_all('tr')
            for row in schedule_table_rows:
                try:
                    boxscore_element = row.find('td', {'data-stat': 'boxscore'})
                    box_score_url_fragment = boxscore_element.a['href']
                    box_score_url = box_score_base_url + box_score_url_fragment
                    box_score_urls.append(box_score_url)
                except Exception as e:
                    print(e)
                    pass
            return box_score_urls

    def output_box_score_data(self, box_scores, output_file_name):
        with open(output_file_name, 'w') as f:
            json.dump(box_scores, f)
