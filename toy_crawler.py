from urllib.request import urlopen
import match_info_extractor as mie

def crawl_url(url):
    response = urlopen(url)
    # Get website in bytes
    htmlbytes = response.read()
    # Replace Turkish characters with question mark (?)
    html_output_str = htmlbytes.decode('utf-8', errors='replace')
    return html_output_str

def toy_TFF_match_crawler():
    # There are certain patterns in the website, this code will try to capture
    # the information we need based on observed patterns
    # 'stadId=11">ANKARA 19 MAYIS<' ('stadId' occurs only once)
    for i in range(2,10):
        url = 'http://www.tff.org/Default.aspx?pageID=29&macId=' + str(i)
        print('Getting:', url)
        match_site_str = crawl_url(url)
        hakem_ids, hakem_names = mie.find_hakemler(match_site_str)
        for name in hakem_names:
            print('Hakem:', name)
        stad_id, stad_name = mie.find_stad(match_site_str)
        print('Stad:', stad_name)
