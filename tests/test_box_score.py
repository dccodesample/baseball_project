from src.BoxScore import BoxScore
import json


def test_calculate_blown_lead_no_blown_leads():
    with open('tests/test_data/no_blown_leads.json', 'r') as f:
        box_score_file = json.load(f)
    for team in box_score_file:
        for season in box_score_file[team]:
            for box_score_id in box_score_file[team][season]:
                box_score_data = box_score_file[team][season][box_score_id]
    test_box_score = BoxScore(box_score_data, box_score_id, season, team)
    assert test_box_score.blown_leads == 0


def test_calculate_one_home_blown_lead():
    with open('tests/test_data/one_home_blown_lead.json', 'r') as f:
        box_score_file = json.load(f)
    for team in box_score_file:
        for season in box_score_file[team]:
            for box_score_id in box_score_file[team][season]:
                box_score_data = box_score_file[team][season][box_score_id]
    test_box_score = BoxScore(box_score_data, box_score_id, season, team)
    assert test_box_score.blown_leads == 1


def test_calculate_one_away_blown_lead():
    with open('tests/test_data/one_away_blown_lead.json', 'r') as f:
        box_score_file = json.load(f)
    for team in box_score_file:
        for season in box_score_file[team]:
            for box_score_id in box_score_file[team][season]:
                box_score_data = box_score_file[team][season][box_score_id]
    test_box_score = BoxScore(box_score_data, box_score_id, season, team)
    assert test_box_score.blown_leads == 1

# Both sides blown lead (one)
# Home blown lead only (multiple)
# Away blown lead only (multiple)
# Both sides blown lead (onmultiplee)
# nearly blown lead (home)
# nearly blown lead (away)
# barely blown lead (home)
# barely blown lead (away)
# barely blown lead (both)
# huge blown lead (home)
# huge blown lead (away)
# huge blown lead (both)
# with no bottom half of final inning
# blown lead in last inning (home)
# blown lead in last inning (away)
# blown lead across multiple innings (home)
# blown lead across multiple innings (away)
# blown lead in one inning, but seperated (got lead in first, lost it in the fifth) (home)
# blown lead in one inning, but seperated (got lead in first, lost it in the fifth) (away)
# tie lead
# eclipse lead
