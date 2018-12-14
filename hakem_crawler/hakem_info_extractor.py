NAME_SEARCH_STR = 'HakemBilgi_Label1">'
OCCUPATION_SEARCH_STR = 'HakemBilgi_Label2">'
LISANS_SEARCH_STR = 'HakemBilgi_Label3">'
KLASMAN_SEARCH_STR = 'HakemBilgi_Label4">'
AREA_SEARCH_STR = 'HakemBilgi_Label6">'

SEARCH_MAX = 100

def get_data_from_html(html_output_str, search_str):
    # HakemBilgi_Label1">FATİH ÖLMEZ<
    # HakemBilgi_Label2">Öğrenci<
    # HakemBilgi_Label3">29864<
    # HakemBilgi_Label4">İl Hakemi<
    # HakemBilgi_Label6">İSTANBUL<
    end_character = '<'
    idx = html_output_str.find(search_str)
    # Get a substring that is long enough
    start_idx = idx + len(search_str)
    end_idx = idx + len(search_str) + SEARCH_MAX
    long_string = html_output_str[start_idx:end_idx]
    # Return from beginning to the point where '<' is
    desired_part = long_string[0:long_string.find(end_character)]
    # Remove extra whitespace from the desired part
    desired_part = ' '.join(desired_part.split())
    return desired_part

def find_name(html_output_str):
    return get_data_from_html(html_output_str, NAME_SEARCH_STR)

def find_occupation(html_output_str):
    return get_data_from_html(html_output_str, OCCUPATION_SEARCH_STR)

def find_lisans_number(html_output_str):
    return int(get_data_from_html(html_output_str, LISANS_SEARCH_STR))

def find_klasman(html_output_str):
    return get_data_from_html(html_output_str, KLASMAN_SEARCH_STR)

def find_area(html_output_str):
    return get_data_from_html(html_output_str, AREA_SEARCH_STR)

####

HAKEM_URL_BASE = 'http://www.tff.org/Default.aspx?pageId=72&hakemId='

def get_hakem_url_string_from_int(hakem_id):
    return HAKEM_URL_BASE + str(hakem_id)
