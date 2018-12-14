import hakem_csv_tools
import hakem_info_extractor
import TFF_hakem

import queue
import threading
import csv
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

DEFAULT_MATCH_INPUT_FILENAME = '/home/folmez/Dropbox/Documents/WWW/not_public/sample_matches_1000_1010.csv'
THREAD_OPEN_WAIT = 10
lock = threading.Lock()

def threaded_crawler(num_worker_threads, silent=False, \
                use_selenium=False, match_input_filename=DEFAULT_MATCH_INPUT_FILENAME):
    # Get hakem output filename
    hakem_output_filename = match_input_filename[:-4] + '_HAKEMLER.csv'

    # Create hakem ID queue and fill it
    hakem_id_queue = queue.Queue()
    hakem_list = hakem_csv_tools.get_hakem_id_from_match_output(match_input_filename)
    for hakem_id in hakem_list:
        hakem_id_queue.put(hakem_id)

    # Write the header row into the hakem output file
    header_row = hakem_csv_tools.get_header_row()
    with open(hakem_output_filename, 'w') as f:
        file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_row)

    # Create crawler workers
    crawler_threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=crawler_worker, args=(hakem_id_queue,\
                                                          hakem_output_filename,\
                                                          silent, use_selenium))
        t.daemon = True
        t.start()
        crawler_threads.append(t)
        time.sleep(THREAD_OPEN_WAIT)

    # Block the main thread until workers processed everything
    hakem_id_queue.join()
    print('Hakem queue has been completely crawled.')

    # Stop crawler workers
    print('Stopping crawlers...')
    for t in crawler_threads:
        t.join()
    print('All crawlers stopped.')

# Single crawler worker, to be used in the threaded module
def crawler_worker(hakem_id_queue, hakem_output_filename, silent, use_selenium=False):
    # open a browser
    driver_path = '/usr/lib/chromium-browser/chromedriver'
    browser = webdriver.Chrome(driver_path)
    time.sleep(THREAD_OPEN_WAIT)

    while not hakem_id_queue.empty():
        hakem_id = hakem_id_queue.get()
        hakem_url = hakem_info_extractor.get_hakem_url_string_from_int(hakem_id)

        print('Getting:', hakem_url)
        SELENIUM_WAIT_TIMEOUT = 20
        short_wait = 2
        k = 0
        browser.get(hakem_url)
        while True:
            k = k + 1
            time.sleep(short_wait)
            inner_HTML = browser.execute_script("return document.body.innerHTML")
            if this_is_a_good_html(inner_HTML) or \
                                this_is_an_error_page(inner_HTML) or \
                                k == SELENIUM_WAIT_TIMEOUT/short_wait:
                break
        hakem_site_str = inner_HTML

        if this_is_an_error_page(hakem_site_str):
            if not silent:
                print('This URL goes to error page: ', hakem_url)
            hakem_output = None # invalid URL
        elif not this_is_a_good_html(hakem_site_str):
            if not silent:
                print('This page is not recognized: ', hakem_url)
            hakem_output = None # unrecognized content
        else:
            this_hakem = TFF_hakem.hakem(hakem_site_str, hakem_id)
            this_hakem.print_summary(silent)
            hakem_output = this_hakem.all_info_in_one_line()

        hakem_id_queue.task_done()

        # Write match output to a new file with thread lock
        if hakem_output is not None:
            lock.acquire()
            with open(hakem_output_filename, 'a') as f:
                file_writer = csv.writer(f, delimiter=',', \
                                            quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([hakem_output])
            lock.release()

    browser.close()

def this_is_a_good_html(html_output_str):
    return hakem_info_extractor.NAME_SEARCH_STR in html_output_str \
            and hakem_info_extractor.OCCUPATION_SEARCH_STR in html_output_str \
            and hakem_info_extractor.LISANS_SEARCH_STR in html_output_str \
            and hakem_info_extractor.KLASMAN_SEARCH_STR in html_output_str \
            and hakem_info_extractor.AREA_SEARCH_STR in html_output_str

def this_is_an_error_page(html_output_str):
    error_indicator = 'Images/TFF/Error/tff.hatalogosu.gif'
    return error_indicator in html_output_str
