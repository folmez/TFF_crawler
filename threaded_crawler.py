import toy_crawler
from queue import Queue
from threading import Thread
import csv

def threaded_crawler(start, stop, num_worker_threads):
    # Create match urls
    match_url_base = 'http://www.tff.org/Default.aspx?pageID=29&macId='
    match_urls = [match_url_base + str(i) for i in range(start, stop + 1)]

    # Create match url queue and fill it
    match_queue = Queue()
    for match in match_urls:
        match_queue.put(match)

    # Create an output queue to write to the CSV file
    output_queue = Queue()

    # Create crawler workers
    for i in range(num_worker_threads):
        t = Thread(target=crawler_worker, args=(match_queue, output_queue, ))
        t.start()

    # Block the main thread until workers processed everything
    match_queue.join()

    # Create a CSV file
    match_output_filename = f"matches_{start}_{stop}.csv"
    with open(match_output_filename, 'w') as f:
        file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['TFF Match ID', 'Tarih', 'Organizasyon', \
                                'Hakem ID', 'Hakem', 'AR1 ID', 'AR1', \
                                'AR2 ID', 'AR2', 'Dort ID', 'Dorduncu Hakem', \
                                'Stad', 'Ev', 'Ev ID', \
                                'Deplasman', 'Deplasman ID', \
                                'Ev skor', 'Deplasman skor'])
        while not output_queue.empty():
            match_output = output_queue.get()
            file_writer.writerow([match_output])
            output_queue.task_done()

# Single crawler worker, to be used in the threaded module
def crawler_worker(match_queue, output_queue):
    while not match_queue.empty():
        match_url = match_queue.get()
        toy_crawler. single_TFF_match_url_crawler(match_url, output_queue)
        match_queue.task_done()
