import single_url_crawler
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

    # Create two output queues to write to the CSV file
    successful_output_queue = Queue()
    failed_output_queue = Queue()

    # Create crawler workers
    for i in range(num_worker_threads):
        t = Thread(target=crawler_worker, args=(match_queue, \
                            successful_output_queue, failed_output_queue, ))
        t.start()

    # Block the main thread until workers processed everything
    match_queue.join()

    # Record everything in two CSV's
    filename = 'successfull_matches_' + str(start) + '_' + str(stop) + '.csv'
    header_row = ['TFF Match ID', 'Tarih', 'Organizasyon', 'Hakem ID', \
                    'Hakem', 'AR1 ID', 'AR1', 'AR2 ID', 'AR2', 'Dort ID', \
                    'Dorduncu Hakem', 'Stad ID', 'Stad','Ev', 'Ev ID', \
                    'Deplasman', 'Deplasman ID', 'Ev skor', 'Deplasman skor']
    save_queue_as_CSV(filename, header_row, successful_output_queue)
    filename = 'failed_matches_' + str(start) + '_' + str(stop) + '.csv'
    header_row = ['TFF Match ID']
    save_queue_as_CSV(filename, header_row, failed_output_queue)

#   DELETE LATER
#    with open(match_output_filename, 'w') as f:
#        file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#        file_writer.writerow()
#        # Record successfully obtained match outputs
#        while not successful_output_queue.empty():
#            match_output = successful_output_queue.get()
#            file_writer.writerow([match_output])
#            successful_output_queue.task_done()

# Single crawler worker, to be used in the threaded module
def crawler_worker(match_queue, successful_output_queue, failed_output_queue):
    while not match_queue.empty():
        match_url = match_queue.get()
        single_url_crawler.single_TFF_match_url_crawler(match_url, \
                                successful_output_queue, failed_output_queue)
        match_queue.task_done()

# Save queue as CSV
def save_queue_as_CSV(output_filename, header_row, queue_to_be_saved):
    with open(output_filename, 'w') as f:
        file_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONE)
        file_writer.writerow(header_row)
        while not queue_to_be_saved.empty():
            output = queue_to_be_saved.get()
            file_writer.writerow([output])
            queue_to_be_saved.task_done()
