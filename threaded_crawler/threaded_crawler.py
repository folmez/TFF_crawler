import match_csv_tools
import match_info_extractor_tools as mie
# import crawler
import TFF_match

import queue
import threading
import csv
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MATCH_OUTPUT_TEST = 'matches_new_file.csv'
THREAD_OPEN_WAIT = 10
lock = threading.Lock()

def threaded_crawler(start, stop, num_worker_threads, silent=False, \
                use_selenium=False, match_output_filename=MATCH_OUTPUT_TEST):
    # Create match ID queue and fill it
    match_id_queue = queue.Queue()

    if match_output_filename is MATCH_OUTPUT_TEST:
        # if a partial match output file is not provided, create a new one
        for match_id in range(start, stop+1):
            match_id_queue.put(match_id)
        header_row = match_csv_tools.get_header_row()
        with open(MATCH_OUTPUT_TEST, 'w') as f:
            file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(header_row)
    else:
        # if provided, then ignore existing match ids in queing
        missing_match_ids = match_csv_tools.get_missing_match_ids_in_range(\
                                            start, stop, match_output_filename)
        for match_id in missing_match_ids:
            match_id_queue.put(match_id)

    # Create crawler workers
    crawler_threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=crawler_worker, args=(match_id_queue,\
                                                          match_output_filename,\
                                                          silent, use_selenium))
        t.daemon = True
        t.start()
        crawler_threads.append(t)
        time.sleep(THREAD_OPEN_WAIT)

    # Block the main thread until workers processed everything
    match_id_queue.join()
    print('Match queue has been completely crawled.')

    # Stop crawler workers
    print('Stopping crawlers...')
    for t in crawler_threads:
        t.join()
    print('All crawlers stopped.')

# Single crawler worker, to be used in the threaded module
def crawler_worker(match_id_queue, match_output_filename, silent, use_selenium=False):
    # open a browser
    driver_path = '/usr/lib/chromium-browser/chromedriver'
    browser = webdriver.Chrome(driver_path)
    time.sleep(THREAD_OPEN_WAIT)

    while not match_id_queue.empty():
        match_id = match_id_queue.get()
        match_url = mie.get_match_url_string_from_int(match_id)

        print('Getting #' + str(match_id) + ':', match_url)
        SELENIUM_WAIT_TIMEOUT = 20
        short_wait = 2
        k = 0
        browser.get(match_url)
        while True:
            k = k + 1
            time.sleep(short_wait)
            inner_HTML = browser.execute_script("return document.body.innerHTML")
            if this_is_a_good_html(inner_HTML) or \
                                k == SELENIUM_WAIT_TIMEOUT/short_wait:
                break
        match_site_str = inner_HTML

        if not this_is_a_good_html(match_site_str):
            if not silent:
                print('This URL does not correspond to a match: ', match_url)
            match_output = None #'Invalid URL'
        else:
            this_match = TFF_match.match(match_site_str)
            this_match.print_summary(silent)
            match_output = this_match.all_info_in_one_line()

        match_id_queue.task_done()

        # Write match output to a new file with thread lock
        if match_output is not None:
            lock.acquire()
            with open(match_output_filename, 'a') as f:
                file_writer = csv.writer(f, delimiter=',', \
                                            quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([match_output])
            lock.release()

    browser.close()

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
