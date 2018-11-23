# TFF_crawler
> python3 -c 'import threaded_crawler as thc; thc.threaded_crawler(2,1000,40)'

November 18, 2018: First working prototype. All little bugs are solve. This script currently should be able to download 100k matches in a couple hours.
November 16, 2018: Crawling is now threaded. > python3 -c 'import threaded_crawler as thc; thc.threaded_crawler(2,1000,40)', this would cover almost 1000 pages in chunks of 40 threads.


Exceptions
1)  Exception: No match time.
    e.g. http://www.tff.org/Default.aspx?pageID=29&macId=49400
    Solution: Assume it is played at noon.

TO-DO
1)
