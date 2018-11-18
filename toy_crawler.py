#!/usr/bin/#!/usr/bin/env python3


from urllib.request import urlopen
from queue import Queue
import match_info_extractor as mie
import TFF_match

# url = 'http://www.tff.org/Default.aspx?pageID=29&macId=' + str(i)
def single_TFF_match_url_crawler(url, output_queue):
    # There are certain patterns in the website, this code will try to capture
    # the information we need based on observed patterns
    # 'stadId=11">ANKARA 19 MAYIS<' ('stadId' occurs only once)
    TFF_match_id_int = int(url[url.find('macId=') + len('macID=')::])
    print('Getting #' + str(TFF_match_id_int) + ':', url)
    # Download website
    match_site_str = crawl_url(url)

    if html_output_is_invalid(match_site_str):
        print('This URL does not correspond to a match.')
    else:
        # Get data and put it into the output queue
        this_match = TFF_match.match(match_site_str)
        this_match.print_summary()
        output_queue.put(this_match.all_info_in_one_line())

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
    return 'Images/TFF/Error/tff.hatalogosu' in html_output_str
