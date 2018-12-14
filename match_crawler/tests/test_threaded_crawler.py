import threaded_crawler
import pytest

@pytest.mark.skip
def test_threaded_crawler():
    start = 2   # start match id
    stop = 11   # stop  match id
    num_worker_threads = stop - start + 1
    use_selenium = True
    threaded_crawler.threaded_crawler(start, stop, num_worker_threads, \
                                    silent=False, use_selenium=use_selenium)
