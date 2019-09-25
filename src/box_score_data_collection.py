# TODO: logging, Error handling, formatting, efficiency, clarity, comment code last
from utils.mlb_project_config_utils import MlbTeamConfigUtils
from utils.mlb_project_web_scraping_utils import MlbWebScrapingUtils
import logging


# sets up the python logging object
logging.basicConfig(format='%(asctime)s - %(filename)s - %(module)s - %(lineno)d - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()
logger.info('STARTING: Data Collection')

years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]

# collects team abbreviations
logger.info('STARTING: Collecting team abbreviations')
team_config_file_object = MlbTeamConfigUtils('config/mlb_config_data.json')
team_abbrvs = team_config_file_object.get_team_abbrvs()
logger.info('FINISHED: Collecting team abbreviations')

# generate home page urls for each team for each year
logger.info(f'STARTING: Generating home page urls for {len(team_abbrvs)} teams for seasons {years[0]}-{years[-1]}')
web_scraper = MlbWebScrapingUtils(team_abbrvs, years, 'https://www.baseball-reference.com/teams')
home_page_urls = web_scraper.url_generator()
logger.info(f'FINISHED: Generating home page urls for {len(home_page_urls.keys())} teams for seasons {years[0]}-{years[-1]}')

# get all the box score urls for each team for all given years
logger.info(f'STARTING: Collecting box score urls for each team for seasons {years[0]}-{years[-1]}')
box_score_base_url = 'https://www.baseball-reference.com/'
box_score_urls = web_scraper.collect_box_score_urls(home_page_urls, box_score_base_url)
logger.info(f'FINISHED: Collecting box score urls for each team for seasons {years[0]}-{years[-1]}')

# get all box score data for each team for all given years
logger.info(f'STARTING: Collecting box score data for each team for seasons {years[0]}-{years[-1]}')
box_scores = web_scraper.collect_box_scores(box_score_urls)
logger.info(f'FINISHED: Collecting box score data for each team for seasons {years[0]}-{years[-1]}')

# write the box score data to a datafile
logger.info('Outputting collected box score data')
web_scraper.output_box_score_data(box_scores, 'data/box_score_data.json')
logger.info('FINISHED: Data Collection')
