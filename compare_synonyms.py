import nltk
import json
import os
import os.path as osp

nltk.download('wordnet')
from nltk.corpus import wordnet

SCRIPT_DIR = osp.dirname(__file__)

'''returns 10 synonyms of word'''
def get_synonyms(word):
    syn = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            syn.add(lemma.name())
    return (list(syn))[:10]


'''get all target words from list'''


def get_targets(in_list):
    targets = []
    for obj in in_list:
        targets.append(obj['word'])
    return targets


'''loads json file'''


def load_json(in_file):
    with open(in_file, 'r') as f:
        data = json.load(f)
    return data


'''compares synonyms of target words with results of ol/ww on description of target words
   for each target word calculates how many synonyms of target word are in results of model on that word 
'''


def compare_syn(targets, results):
    score = []
    score_10 = []
    score_25 = []
    score_50 = []

    for i, result in enumerate(results):
        # result is list of 100 words
        cur_synonyms = get_synonyms(targets[i])  # synonyms of target of current iteration

        cur_score = 0
        cur_score10 = 0
        cur_score25 = 0
        cur_score50 = 0

        for word in cur_synonyms:
            if word in result[:10] and word != targets[i]:
                weight = result[:10].index(word)
                # cur_score10 += 10 - weight
                cur_score10 += 1

        for word in cur_synonyms:
            if word in result[:25] and word != targets[i]:
                weight = result[:25].index(word)
                # cur_score25 += (25 - weight) // 2.5
                cur_score25 += 1

        for word in cur_synonyms:
            if word in result[:50] and word != targets[i]:
                weight = result[:50].index(word)
                # cur_score50 += (50 - weight) // 5
                cur_score50 += 1

        for word in cur_synonyms:
            if word in result and word != targets[i]:
                weight = result.index(word)
                # cur_score += (100 - weight) // 10
                cur_score += 1

        score_10.append(cur_score10)
        score_25.append(cur_score25)
        score_50.append(cur_score50)
        score.append(cur_score)

    scores = [score_10, score_25, score_50, score]
    avg_scores = [sum(score) / len(score) for score in scores]
    return avg_scores


def main():
    # get target words from each data file
    data_desc = osp.join(SCRIPT_DIR, 'data', 'data_desc_c.json')
    data_desc = load_json(data_desc)
    data_desc_targets = get_targets(data_desc)

    seen_500 = osp.join(SCRIPT_DIR, 'data', 'data_test_500_rand1_seen.json')
    seen_500 = load_json(seen_500)
    seen_500_targets = get_targets(seen_500)

    unseen_500 = osp.join(SCRIPT_DIR, 'data', 'data_test_500_rand1_unseen.json')
    unseen_500 = load_json(unseen_500)
    unseen_500_targets = get_targets(unseen_500)

    # get results of each model on targets
    data_desc_rww = osp.join(SCRIPT_DIR, 'results', 'data_desc_results_ww.json')
    data_desc_rww = load_json(data_desc_rww)

    data_desc_rol = osp.join(SCRIPT_DIR, 'results', 'data_desc_results_ol.json')
    data_desc_rol = load_json(data_desc_rol)

    seen_500_rww = osp.join(SCRIPT_DIR, 'results', 'data_seen_results_ww.json')
    seen_500_rww = load_json(seen_500_rww)

    seen_500_rol = osp.join(SCRIPT_DIR, 'results', 'data_seen_results_ol.json')
    seen_500_rol = load_json(seen_500_rol)

    unseen_500_rww = osp.join(SCRIPT_DIR, 'results', 'data_unseen_results_ww.json')
    unseen_500_rww = load_json(unseen_500_rww)

    unseen_500_rol = osp.join(SCRIPT_DIR, 'results', 'data_unseen_results_ol.json')
    unseen_500_rol = load_json(unseen_500_rol)

    print(compare_syn(data_desc_targets, data_desc_rww))
    print(compare_syn(data_desc_targets, data_desc_rol))
    print("*" * 20)
    print(compare_syn(seen_500_targets, seen_500_rww))
    print(compare_syn(seen_500_targets, seen_500_rol))
    print("*" * 20)
    print(compare_syn(unseen_500_targets, unseen_500_rww))
    print(compare_syn(unseen_500_targets, unseen_500_rol))


if __name__ == '__main__':
    main()
