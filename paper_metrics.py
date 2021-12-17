import json
import os.path as osp

desc = "data_desc_c.json"
unseen = "data_test_500_rand1_unseen.json"
seen = "data_test_500_rand1_seen.json"
desc_r = "data_desc_results"
unseen_r = "data_unseen_results"
seen_r = "data_seen_results"
ww = "_ww.json"
ol = "_ol.json"

data = json.load(open(osp.join("data", desc), "r"))
results = json.load(open(osp.join("results", desc_r + ol), "r"))
total = len(results)
indexes = []
top_1 = 0
top_10 = 0
top_100 = 0

for i in range(total):
    for j in range(len(results[i])):
        results[i][j] = str.lower(results[i][j])

for i in range(total):
    # if i < 10:
    #     print(data[i]["word"])
    try:
        index = results[i].index(str.lower(data[i]["word"]))
        if i < 10:
            print(data[i]["word"])

        indexes.append(index+1)
        if index < 100:
            top_100 += 1
        if index < 10:
            top_10 += 1
        if index < 1:
            top_1 += 1
    except:
        continue

# median rank
print(f'median: {sum(indexes) / len(indexes)}')
# top 1/10/100
print(f'top 1: {top_1 / total}')
print(f'top 10: {top_10 / total}')
print(f'top 100: {top_100 / total}')

# median: 7.151351351351352
# top 1: 0.415
# top 10: 0.795
# top 100: 0.925
