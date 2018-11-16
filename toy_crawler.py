from urllib.request import urlopen
from queue import Queue
import match_info_extractor as mie

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
        # Get data
        hakem_ids, hakem_names = mie.find_hakemler(match_site_str)
        stad_id, stad_name = mie.find_stad(match_site_str)
        # Pring extracted data from the url
        TFF_match_id_str = f"[TFF Match #{TFF_match_id_int}] "
        for name in hakem_names:
            print(TFF_match_id_str, 'Hakem:', name)
        print(TFF_match_id_str, 'Stad:', stad_name)
        match_output = str(TFF_match_id_int) + ',' + hakem_names[0] +\
                            ',' + stad_name
        output_queue.put(match_output)

def crawl_url(url):
    response = urlopen(url)
    # Get website in bytes
    htmlbytes = response.read()
    # Replace Turkish characters with question mark (?)
    html_output_str = htmlbytes.decode('utf-8', errors='replace')
    return html_output_str

def html_output_is_invalid(html_output_str):
    # 'Images/TFF/Error/tff.hatalogosu' seems to be the a unique error identifier
    return 'Images/TFF/Error/tff.hatalogosu' in html_output_str
