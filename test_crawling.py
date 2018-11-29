#!/usr/bin/#!/usr/bin/env python3
from TFF_crawler import crawl_url, html_output_is_invalid

TEST_URL = 'http://www.tff.org/Default.aspx?pageID=29&macId=2'

def test_crawl_url():
    html_output_str = crawl_url(TEST_URL, use_selenium=True)
    assert html_output_is_invalid(html_output_str) is False
