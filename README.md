# TFF_crawler
> python3 -c 'import threaded_crawler as thc; thc.threaded_crawler(2,1000,40)'

November 18, 2018: First working prototype. All little bugs are solve. This script currently should be able to download 100k matches in a couple hours.
November 16, 2018: Crawling is now threaded. > python3 -c 'import threaded_crawler as thc; thc.threaded_crawler(2,1000,40)', this would cover almost 1000 pages in chunks of 40 threads.


Exceptions
1) In rare cases, there is no score. In these cases, score is considered -1
2) tff.org/Default.aspx?pageID=29&macId=5049 - International Match
3) Think about how to deal with exceptions

TO-DO
1) 
