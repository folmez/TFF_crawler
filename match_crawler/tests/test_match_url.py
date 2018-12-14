import match_info_extractor_tools as mie

def test_get_match_url_string_from_int():
    assert mie.get_match_url_string_from_int(1) == \
                            'http://www.tff.org/Default.aspx?pageID=29&macId=1'
