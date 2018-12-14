import hakem_info_extractor

def test_get_hakem_url_string_from_int():
    assert hakem_info_extractor.get_hakem_url_string_from_int(18626) == \
                    'http://www.tff.org/Default.aspx?pageId=72&hakemId=18626'
