from queue import Queue
import threading
import csv
import match_info_extractor as mie
from urllib.request import urlopen, Request
import TFF_match
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MATCH_URL_BASE = 'http://www.tff.org/Default.aspx?pageID=29&macId='
MATCH_OUTPUT_TEST = 'matches_new_file.csv'
SELENIUM_WAIT_TIMEOUT = 20 # seconds
lock = threading.Lock()

def threaded_crawler(start, stop, num_worker_threads, silent=False, \
                use_selenium=False, match_output_filename=MATCH_OUTPUT_TEST):
    # Create match ID queue and fill it
    match_id_queue = Queue()

    if match_output_filename is MATCH_OUTPUT_TEST:
        # if a partial match output file is not provided, create a new one
        for match_id in range(start, stop+1):
            match_id_queue.put(match_id)
        header_row = get_header_row()
        with open(MATCH_OUTPUT_TEST, 'w') as f:
            file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(header_row)
    else:
        # if provided, then ignore existing match ids in queing
        # WRITE A SMALL SCRIPT TO GET EXISTING MATHCES AND MISSING MATCHES
        pass

    # Create crawler workers
    crawler_threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=crawler_worker, args=(match_id_queue, \
                                                        silent, use_selenium))
        t.daemon = True
        t.start()
        crawler_threads.append(t)

    # Block the main thread until workers processed everything
    match_id_queue.join()
    print('Match queue has been completely crawled.')

    # Stop crawler workers
    print('Stopping crawlers...')
    for t in crawler_threads:
        t.join()
    print('All crawlers stopped.')

# Single crawler worker, to be used in the threaded module
def crawler_worker(match_id_queue, silent, use_selenium=False):
    while not match_id_queue.empty():
        match_id = match_id_queue.get()
        match_url = get_match_url_string_from_int(match_id)
        match_output = single_TFF_match_url_crawler(match_url, silent, \
                                                                use_selenium)
        match_id_queue.task_done()

        # Write match output to a new file with thread lock
        if match_output is not None:
            lock.acquire()
            with open(MATCH_OUTPUT_TEST, 'a') as f:
                file_writer = csv.writer(f, delimiter=',', \
                                            quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([match_output])
            lock.release()

# url = 'http://www.tff.org/Default.aspx?pageID=29&macId=' + str(i)
def single_TFF_match_url_crawler(url, silent=False, use_selenium=False):
    # There are certain patterns in the website, this code will try to capture
    # the information we need based on observed patterns
    # 'stadId=11">ANKARA 19 MAYIS<' ('stadId' occurs only once)
    TFF_match_id_int = int(url[url.find('macId=') + len('macID=')::])
    print('Getting #' + str(TFF_match_id_int) + ':', url)

    # Download website
    match_site_str = crawl_url(url, use_selenium)

    # Crunch the website html
    if html_output_is_invalid(match_site_str):
        # Put mac id into the failed queue
        if not silent:
            if mie.access_blocked(match_site_str):
                print('ACCESS BLOCKED BY TFF.ORG!')
            else:
                print('This URL does not correspond to a match: ', url)
        return None #'Invalid URL'
    else:
        # Get data and put it into the output queue
        this_match = TFF_match.match(match_site_str)
        this_match.print_summary(silent)
        return this_match.all_info_in_one_line()

def crawl_url(url, use_selenium=False):
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

def html_output_is_invalid(html_output_str):
    return not mie.this_is_a_good_html(html_output_str)
#    # 'Images/TFF/Error/tff.hatalogosu' seems to be the a unique error identifier
#    return 'Images/TFF/Error/tff.hatalogosu' in html_output_str or \
#            'Esame Bilgileri Kulüpler Tarafından Girilmektedir' in html_output_str or \
#            'ÖZEL MAÇ' in html_output_str or \
#            not mie.this_is_a_good_html(html_output_str)

def get_header_row():
    return ['TFF Match ID', 'Tarih', 'Organizasyon', 'Hakem ID', \
                    'Hakem', 'AR1 ID', 'AR1', 'AR2 ID', 'AR2', 'Dort ID', \
                    'Dorduncu Hakem', 'Stad ID', 'Stad','Ev', 'Ev ID', \
                    'Deplasman', 'Deplasman ID', 'Ev skor', 'Deplasman skor']

def get_match_url_string_from_int(match_id):
    return MATCH_URL_BASE + str(match_id)
