import json
import pandas as pd
from BoxScore import BoxScore


with open('data/box_score_data.json', 'r') as f:
    box_score_data = json.load(f)

df = pd.DataFrame()
for team in box_score_data:
    for season in box_score_data[team]:
        for box_score_id in box_score_data[team][season]:
            box_score_raw = box_score_data[team][season][box_score_id]
            box_score = BoxScore(box_score_raw, box_score_id, season, team)

            columns = list(box_score.__dict__.keys())
            values = list(box_score.__dict__.values())
            temp_data_frame = pd.DataFrame([values], columns=columns)
            df = df.append(temp_data_frame)

            # print(temp_data_frame)

            break
        break
    # break
print(df)

# dataframe = pd.DataFrame(box_score_data['2012'])
# for team in box_score_data:
#     team_data_frame = pd.DataFrame()
#     for season in box_score_data[team]:
#         season_data_frame = pd.DataFrame(box_score_data[team][season])
#         print(season_data_frame)
#         break
        # print(box_score_data[team][season])
        # team_data_frame.append()

# x = 5
# df = pd.DataFrame([1, 2, 3, 'a'])
# df2 = pd.DataFrame([4])
# print(df)
# df = df.append(df2, ignore_index=True)
# print(df)