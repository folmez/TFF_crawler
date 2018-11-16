import toy_crawler
from queue import Queue
from threading import Thread

# Single crawler worker, to be used in the threaded module
def crawler_worker(match_queue):
    while not match_queue.empty():
        match_url = match_queue.get()
        toy_crawler.single_TFF_match_url_crawler(match_url)
        match_queue.task_done()

def threaded_crawler(start, stop, num_worker_threads):
    # Create match urls
    match_url_base = 'http://www.tff.org/Default.aspx?pageID=29&macId='
    match_urls = [match_url_base + str(i) for i in range(start, stop + 1)]

    # Create match url queue and fill it
    match_queue = Queue()
    for match in match_urls:
        match_queue.put(match)

    # Create crawler workers
    for i in range(num_worker_threads):
        t = Thread(target=crawler_worker, args=(match_queue, ))
        t.start()
    
    match_queue.join()

#def worker():
#    while True:
#        item = q.get()
#        do_work(item)
#        q.task_done()

#q = Queue()
#for i in range(num_worker_threads):
#     t = Thread(target=worker)
#     t.daemon = True
#     t.start()

#for item in source():
#    q.put(item)

#q.join()       # block until all tasks are done
