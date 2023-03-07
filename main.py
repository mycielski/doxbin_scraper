import random
import sys

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm

BASE_URL = "https://doxbin.net/"
DOX_XPATH = """//tr[contains(@class, 'doxentry')]/*/a[@href and @title and not(contains(@class, 'dox-username'))]"""
DOX_BODY_XPATH = """//pre[@style]"""
IGNORE_TITLES = [
    "764",
    "Biloo Dox By Zalko",
    "How to Ensure Your Paste Stays Up",
    "Transparency Report",
]
TARGET_DIR = "output"
EXTENSION = "txt"
LAST_PAGE = 624


def main() -> int:
    options = selenium.webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--incognito")
    browser = webdriver.Chrome(options=options)

    pages = [i for i in range(1, LAST_PAGE + 1)]
    # scramble the order of the pages
    random.shuffle(pages)

    for i in tqdm(pages):
        browser.get(BASE_URL + f"?page={i}")

        doxes = browser.find_elements(By.XPATH, DOX_XPATH)

        links_and_titles = [
            (dox.get_attribute("href"), dox.get_attribute("title"))
            for dox in doxes
            if dox.get_attribute("title") not in IGNORE_TITLES
        ]

        for link, title in tqdm(links_and_titles):
            browser.get(link)
            dox_body = browser.find_element(By.XPATH, DOX_BODY_XPATH)

            with open(f"{TARGET_DIR}/{title}.{EXTENSION}", "w") as f:
                f.write(dox_body.text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
