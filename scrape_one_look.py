import json
import os.path as osp
import bs4
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

URL_BASE = "https://www.onelook.com/thesaurus/?s="


def get_words(sentence, browser, sleep_time):
    sentence = sentence.replace(" ", "%20")

    browser.get(URL_BASE + sentence)
    time.sleep(sleep_time)

    results_html = browser.page_source

    soup = bs4.BeautifulSoup(results_html, "html.parser")
    results = []
    for i in range(1, 101):
        result = soup.find("div", {"resid": str(i)})
        if result:
            result = result.attrs["thesw"].replace("%20", " ")
            results.append(result)

    # print(len(results))
    return results


def get_all_results(data, browser):
    all_results = []
    for obj in data:
        words = get_words(obj["definitions"], browser, 2)
        try:
            print(f'{obj["word"]}: {words[0]}')
            all_results.append(words)
        except:
            words = get_words(obj["definitions"], browser, 4)
            try:
                print(f'{obj["word"]}: {words[0]}')
                all_results.append(words)
            except:
                print("do manually")
    return all_results


def get_results_user_gen(data, browser):
    all_results = []
    for obj in data:
        words = get_words(obj, browser, 2)
        try:
            print(f'{obj}: {words[0:3]}')
            all_results.append(words)
        except:
            words = get_words(obj, browser, 4)
            try:
                print(f'{obj}: {words[0:3]}')
                all_results.append(words)
            except:
                print("do manually")
    return all_results


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    with open(osp.join("data", "data_desc_c.json"), "r") as file:
        data = json.load(file)
    with open(osp.join("results", "data_desc_results_ol.json"), "w") as output:
        json.dump(get_all_results(data, browser), output)

    print("...collected data for desc...\n...moving on to unseen data...")

    with open(osp.join("data", "data_test_500_rand1_unseen.json"), "r") as file:
        data = json.load(file)
    with open(osp.join("results", "data_unseen_results_ol.json"), "w") as output:
        json.dump(get_all_results(data, browser), output)

    print("...collected data for unseen...\n...moving on to seen data...")

    with open(osp.join("data", "data_test_500_rand1_seen.json"), "r") as file:
        data = json.load(file)
    with open(osp.join("results", "data_seen_results_ol.json"), "w") as output:
        json.dump(get_all_results(data, browser), output)

    with open(osp.join("data", "user_gen_defs.txt"), "r") as file:
        data = file.read().splitlines()
        print(data[0])
    with open(osp.join("results", "user_gen_defs_results_ol.json"), "w") as output:
        json.dump(get_results_user_gen(data, browser), output)


if __name__ == "__main__":
    main()
