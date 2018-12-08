import match_csv_tools
import match_info_extractor_tools as mie
import crawler

from queue import Queue
import threading
import csv

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MATCH_OUTPUT_TEST = 'matches_new_file.csv'
lock = threading.Lock()

def threaded_crawler(start, stop, num_worker_threads, silent=False, \
                use_selenium=False, match_output_filename=MATCH_OUTPUT_TEST):
    # Create match ID queue and fill it
    match_id_queue = Queue()

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
        match_url = mie.get_match_url_string_from_int(match_id)
        match_output = crawler.single_TFF_match_url_crawler(match_url, silent, \
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
