MATCH_URL_BASE = 'http://www.tff.org/Default.aspx?pageID=29&macId='

def get_match_url_string_from_int(match_id):
    return MATCH_URL_BASE + str(match_id)
