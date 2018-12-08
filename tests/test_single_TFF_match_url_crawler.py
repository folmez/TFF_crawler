import pytest
import crawler

NO_MATCH_TEST_LINK = 'http://www.tff.org/Default.aspx?pageID=29&macId=' + '1'

@pytest.mark.slow
def test_single_TFF_match_url_crawler_no_match():
    assert crawler.single_TFF_match_url_crawler(NO_MATCH_TEST_LINK, \
                                    silent=True, use_selenium=True) == None
