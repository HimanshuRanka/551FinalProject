
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
    time.sleep(1) #Switch with proper wait function later
    eng_tab = driver.find_element(By.ID,'ui-id-3') #english tab to make sure using english dictionary
    eng_tab.click()
    return driver
 
'''makes query on want words'''
def query(driver, in_query):
    time.sleep(1)

    #get search bar
    search = driver.find_element(By.ID,'description_EE')

    #search query
    search.send_keys(in_query)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    return driver

'''return list of results from query'''
def results(driver):
    li_list=[]
    items = driver.find_elements(By.TAG_NAME,"ol")
    time.sleep(1)
    for item in items:
        li_list.extend(item.find_elements(By.TAG_NAME,"li"))
        time.sleep(1)
    
    words_list = [item.text for item in li_list]
    return words_list
    

def main():
    driver= webdriver.Chrome(ChromeDriverManager().install()) #, options=chrome_options
    driver.get(URL)
    driver = setup(driver)
    driver = query(driver, "the thing I can use to eat") #test
    time.sleep(1)
    results_list=results(driver)
    print(results_list)
    
    

if __name__ == "__main__":
    main()
