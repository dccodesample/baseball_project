import csv
# team_abbrv
# team_name
# box_score_data
# box_score_id
# season
# home_team
# home_team_innings_data
# home_team_other_data
# away_team
# away_team_innings_data
# away_team_other_data
# team_side
# result
# blow_leads



with open('test1.csv', 'r') as f:
    file_reader = csv.reader(f, delimiter=',')

    file_as_list = []
    for line in file_reader:
        file_as_list.append(line)

for line in file_as_list:
    print(line[-1])
