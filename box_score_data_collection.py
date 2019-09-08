# TODO: Error handling, logging, formatting, efficiency, clarity
# before generate actual full data set, finalize data analysis code (or verify that the data format will work)
from bs4 import BeautifulSoup
import requests
import json

from mlb_project_config_utils import MlbTeamConfigUtils
from mlb_project_web_scraping_utils import MlbWebScrapingUtils

years = ['2012', '2013']
# years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]

# collect team abbreviations
team_config_file_object = MlbTeamConfigUtils('mlb_data_config.json')
team_abbrvs = team_config_file_object.get_team_abbrvs()

# generate home page urls for each team for each year
web_scraper = MlbWebScrapingUtils(team_abbrvs, years, 'https://www.baseball-reference.com/teams')
home_page_urls = web_scraper.url_generator()

# get all the box score urls for each team for all given years
box_score_base_url = 'https://www.baseball-reference.com/'
box_score_urls = web_scraper.collect_box_score_urls(home_page_urls, box_score_base_url)

# get all box score data for each team for all given years
box_scores = web_scraper.collect_box_scores(box_score_urls)

# write the box score data to a datafile
web_scraper.output_box_score_data(box_scores, 'box_score_data.json')
