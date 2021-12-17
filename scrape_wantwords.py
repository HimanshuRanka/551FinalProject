import os.path as osp
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
URL = "https://wantwords.thunlp.org/"

'''Setup website to use english dictionary'''
def setup(driver):
    #Switch with proper wait function later
    eng_tab = driver.find_element(By.ID,'ui-id-3') #english tab to make sure using english dictionary
    eng_tab.click()
    return driver
 
'''makes query on want words'''
def query(driver, in_query):

    #get search bar
    search = driver.find_element(By.ID,'description_EE')

    #search query
    search.send_keys(in_query)

    search.send_keys(Keys.RETURN)
    return driver

'''return list of results from query'''
def results(driver):
    li_list = []
    items = driver.find_elements(By.TAG_NAME,"ol")
    for item in items:
        li_list.extend(item.find_elements(By.TAG_NAME,"li"))
    words_list = [item.text for item in li_list]
    return words_list


def get_all_results(data, driver):
    all_results = []
    for obj in data:
        driver.get(URL)
        driver = setup(driver)
        driver = query(driver, obj["definitions"])  # test
        time.sleep(0.8)
        results_list = results(driver)
        try:
            print(f'{obj["word"]}: {results_list[0]}')
            all_results.append(results_list)
        except:
            driver.get(URL)
            driver = setup(driver)
            driver = query(driver, obj["definitions"])  # test
            time.sleep(1.8)
            results_list = results(driver)
            all_results.append(results_list)
            try:
                print(f'{obj["word"]}: {results_list[0]}')
            except:
                print("fix this manually")
    return all_results


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.set_window_size(1440, 900)
    driver.get(URL)
    driver = setup(driver)
    driver = query(driver, "the thing I can use to eat") #test
    time.sleep(1.5)
    results_list = results(driver)
    print(results_list)
    print(len(results_list))

    with open(osp.join("data", "data_desc_c.json"), "r") as file:
        data = json.load(file)
    with open(osp.join("results", "data_desc_results_ww.json"), "w") as output:
        json.dump(get_all_results(data, driver), output)

    print("...collected data for desc...\n...moving on to unseen data...")

    with open(osp.join("data", "data_test_500_rand1_unseen.json"), "r") as file:
        data = json.load(file)
    with open(osp.join("results", "data_unseen_results_ww.json"), "w") as output:
        json.dump(get_all_results(data, driver), output)

    print("...collected data for unseen...\n...moving on to seen data...")

    with open(osp.join("data", "data_test_500_rand1_seen.json"), "r") as file:
        data = json.load(file)
    with open(osp.join("results", "data_seen_results_ww.json"), "w") as output:
        json.dump(get_all_results(data, driver), output)


if __name__ == "__main__":
    main()
