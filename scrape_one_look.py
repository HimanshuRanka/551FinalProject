import bs4
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_words(sentence):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    URL_BASE = "https://www.onelook.com/thesaurus/?s="
    sentence = sentence.replace(" ", "%20")
    print(sentence)

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    browser.get(URL_BASE + sentence)
    time.sleep(0.55)

    results_html = browser.page_source

    # print(results_html)

    soup = bs4.BeautifulSoup(results_html, "html.parser")
    results = []
    for i in range(1, 11):
        result = soup.find("div", {"resid": str(i)}).attrs["thesw"].replace("%20", " ")
        results.append(result)

    print(results)
    return results

