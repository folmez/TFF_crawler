import match_info_extractor_tools as mie
import TFF_match

from urllib.request import urlopen, Request
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import time

ACCESS_BLOCK_SEARCH_STR = 'Your support ID is'

# Typical TFF match URL:
# 'http://www.tff.org/Default.aspx?pageID=29&macId=' + str(i)

def single_TFF_match_url_crawler(url, silent=False, use_selenium=False):
    TFF_match_id_int = int(url[url.find('macId=') + len('macID=')::])
    print('Getting #' + str(TFF_match_id_int) + ':', url)

    # Download website
    match_site_str = crawl_url(url, use_selenium)

    # Crunch the website html
    if not this_is_a_good_html(match_site_str):
        if not silent:
            if access_blocked(match_site_str):
                print('ACCESS BLOCKED BY TFF.ORG! Are you using Selenium?')
            else:
                print('This URL does not correspond to a match: ', url)
        return None #'Invalid URL'
    else:
        this_match = TFF_match.match(match_site_str)
        this_match.print_summary(silent)
        return this_match.all_info_in_one_line()

def crawl_url(url, use_selenium=False, SELENIUM_WAIT_TIMEOUT = 20):
    if use_selenium:
        driver_path = '/usr/lib/chromium-browser/chromedriver'
        browser = webdriver.Chrome(driver_path)
        browser.get(url)
        time.sleep(SELENIUM_WAIT_TIMEOUT)
        inner_HTML = browser.execute_script("return document.body.innerHTML")
        browser.close()
        return inner_HTML

    else:
        response = urlopen(url)

        # Get website in bytes
        htmlbytes = response.read()
        # Replace Turkish characters with question mark (?)
        # html_output_str = htmlbytes.decode('utf-8', errors='replace')
        html_output_str = htmlbytes.decode('windows-1254')
        return html_output_str

def access_blocked(html_output_str):
    return ACCESS_BLOCK_SEARCH_STR in html_output_str

def this_is_a_good_html(html_output_str):
    return mie.AR2_SEARCH_STR[0] in html_output_str \
            and mie.AR1_SEARCH_STR[0] in html_output_str \
            and mie.HAKEM_SEARCH_STR[0] in html_output_str \
            and mie.AWAY_TEAM_SEARCH_STR[0] in html_output_str \
            and mie.HOME_TEAM_SEARCH_STR[0] in html_output_str \
            and mie.STAD_SEARCH_STR[0] in html_output_str \
            and mie.MAC_ID_SEARCH_STR in html_output_str \
            and mie.ORGANIZASYON_NAME_SEARCH_STR in html_output_str \
            and mie.DATETIME_SEARCH_STR in html_output_str \
            and mie.HOME_TEAM_SKOR_SEARCH_STR in html_output_str \
            and mie.AWAY_TEAM_SKOR_SEARCH_STR in html_output_str
