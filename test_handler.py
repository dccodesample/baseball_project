from tests import test_box_score

d = {'ARI': 0.0, 'ATL': 0.0, 'BAL': 1.0, 'BOS': 0.0, 'CHC': 0.0, 'CHW': 0.0, 'CIN': 1.0, 'CLE': 0.0, 'COL': 0.0, 'DET': 0.0, 'HOU': 0.0, 'KCR': 0.0, 'LAA': 0.0, 'LAD': 0.0, 'MIA': 0.0, 'MIL': 0.0, 'MIN': 0.0, 'NYM': 0.0, 'NYY': 0.0, 'OAK': 0.0, 'PHI': 0.0, 'PIT': 0.0, 'SDP': 0.0, 'SEA': 0.0, 'SFG': 0.0, 'STL': 0.0, 'TBR': 0.0, 'TEX': 0.0, 'TOR': 0.0, 'WSN': 0.0}
print(d)
d['STL_2012'] = d.pop('STL')
print(d)
