from queue import Queue
import threading
import csv
import match_info_extractor as mie
from urllib.request import urlopen
import TFF_match
import time

UNCRAWLED_MATCH_ID_FILE = 'uncrawled_match_id_1_200000.csv'
MATCH_OUTPUT_TEST = 'matches_Nov23_2018.csv'
lock = threading.Lock()

def threaded_crawler(start, stop, num_worker_threads, silent=False):
    # Create match urls
    match_url_base = 'http://www.tff.org/Default.aspx?pageID=29&macId='
    match_urls = [match_url_base + str(i) for i in range(start, stop + 1)]

    # Create match url queue and fill it
    match_queue = Queue()
    for match in match_urls:
        match_queue.put(match)

    # Create two output queues to write to the CSV file
    successful_output_queue = Queue()
    failed_output_queue = Queue()

    # Initiate MATCH_OUTPUT_TEST
    header_row = get_header_row()
    with open(MATCH_OUTPUT_TEST, 'a') as f:
        file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_row)

    # Create crawler workers
    crawler_threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=crawler_worker, args=(match_queue, \
                        successful_output_queue, failed_output_queue, silent, ))
        t.daemon = True
        t.start()
        crawler_threads.append(t)

    manual_ending = False
    if manual_ending:
        input('Did it end yet? ')
    else:
        # Block the main thread until workers processed everything
        match_queue.join()
        print('Match queue has been completely crawled.')

    # Stop crawler workers
    print('Stopping crawlers...')
    for t in crawler_threads:
        t.join()
    print('All crawlers stopped.')

    # Record everything in two CSV's
    print('Recording...')
    filename = 'found_matches_' + str(start) + '_' + str(stop) + '.csv'
    save_queue_as_CSV(filename, header_row, successful_output_queue)
    filename = 'not_found_matches_' + str(start) + '_' + str(stop) + '.csv'
    header_row = ['TFF Match ID']
    save_queue_as_CSV(filename, header_row, failed_output_queue)

# Single crawler worker, to be used in the threaded module
def crawler_worker(match_queue, successful_output_queue, \
                                                failed_output_queue, silent):
    while not match_queue.empty():
        match_url = match_queue.get()
        match_output = single_TFF_match_url_crawler(match_url, \
                        successful_output_queue, failed_output_queue, silent)
        match_queue.task_done()

        # Write match output to a new file with thread lock
        lock.acquire()
        with open(MATCH_OUTPUT_TEST, 'a') as f:
            file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow([match_output])
        lock.release()

# url = 'http://www.tff.org/Default.aspx?pageID=29&macId=' + str(i)
def single_TFF_match_url_crawler(url, successful_output_queue, \
                                            failed_output_queue, silent=False):
    # There are certain patterns in the website, this code will try to capture
    # the information we need based on observed patterns
    # 'stadId=11">ANKARA 19 MAYIS<' ('stadId' occurs only once)
    TFF_match_id_int = int(url[url.find('macId=') + len('macID=')::])
    print('Getting #' + str(TFF_match_id_int) + ':', url)

    # Download website
    match_site_str = crawl_url(url)

    if html_output_is_invalid(match_site_str):
        # Put mac id into the failed queue
        failed_output_queue.put(TFF_match_id_int)
        if not silent:
            print('This URL does not correspond to a match: ', url)
        return 'Invalid URL'
    else:
        # Get data and put it into the output queue
        this_match = TFF_match.match(match_site_str)
        this_match.print_summary(silent)
        match_output = this_match.all_info_in_one_line()
        successful_output_queue.put(match_output)
        return match_output

def crawl_url(url):
    response = urlopen(url)
    # Get website in bytes
    htmlbytes = response.read()
    # Replace Turkish characters with question mark (?)
    # html_output_str = htmlbytes.decode('utf-8', errors='replace')
    html_output_str = htmlbytes.decode('windows-1254')
    return html_output_str

def html_output_is_invalid(html_output_str):
    # 'Images/TFF/Error/tff.hatalogosu' seems to be the a unique error identifier
    return 'Images/TFF/Error/tff.hatalogosu' in html_output_str or \
            'Esame Bilgileri Kulüpler Tarafından Girilmektedir' in html_output_str or \
            'ÖZEL MAÇ' in html_output_str or \
            not mie.this_is_a_good_html(html_output_str)

# Save queue as CSV
def save_queue_as_CSV(output_filename, header_row, queue_to_be_saved):
    with open(output_filename, 'w') as f:
        file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header_row)
        while not queue_to_be_saved.empty():
            output = queue_to_be_saved.get()
            file_writer.writerow([output])
            queue_to_be_saved.task_done()
    print('Saved:', output_filename)

# Generate a CSV file containing match ID's in [start, stop]
def generate_match_id_list_as_CSV(start, stop):
    filename = 'uncrawled_match_id_' + str(start) + '_' + str(stop) + '.csv'
    with open(filename, 'w') as f:
        file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for mac_id in range(start, stop+1):
            file_writer.writerow([mac_id])

# Load uncrawled match IDs into a queue
def load_uncrawled_match_IDs_into_match_url_queue():

    # Create match urls
    match_url_base = 'http://www.tff.org/Default.aspx?pageID=29&macId='
    match_urls = [match_url_base + str(i) for i in range(start, stop + 1)]

    # Create match url queue and fill it
    match_queue = Queue()
    for match in match_urls:
        match_queue.put(match)

def get_header_row():
    return ['TFF Match ID', 'Tarih', 'Organizasyon', 'Hakem ID', \
                    'Hakem', 'AR1 ID', 'AR1', 'AR2 ID', 'AR2', 'Dort ID', \
                    'Dorduncu Hakem', 'Stad ID', 'Stad','Ev', 'Ev ID', \
                    'Deplasman', 'Deplasman ID', 'Ev skor', 'Deplasman skor']
