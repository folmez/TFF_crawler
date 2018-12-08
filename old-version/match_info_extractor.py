import datetime
import sys

SEARCH_MAX = 100

# These search strings are assumed to appear at least once, and have identical
# information no matter how many times they appear
DORT_SEARCH_STR = ['03_lnkHakem', 'hakemId='] # some matches do not have a fourth official, do not assert this
AR2_SEARCH_STR = ['02_lnkHakem', 'hakemId=']
AR1_SEARCH_STR = ['01_lnkHakem', 'hakemId=']
HAKEM_SEARCH_STR = ['00_lnkHakem', 'hakemId=']
AWAY_TEAM_SEARCH_STR = ['Takim2"', 'kulupId=']
HOME_TEAM_SEARCH_STR = ['Takim1"', 'kulupId=']
STAD_SEARCH_STR = ['lnkStad', 'stadId=']

MAC_ID_SEARCH_STR = ';macId='
ORGANIZASYON_NAME_SEARCH_STR = 'MacBilgisi_lblOrganizasyonAdi">'
DATETIME_SEARCH_STR = 'MacBilgisi_lblTarih">'
HOME_TEAM_SKOR_SEARCH_STR = 'Takim1Skor">'
AWAY_TEAM_SKOR_SEARCH_STR = 'Label12">'

ACCESS_BLOCK_SEARCH_STR = 'Your support ID is'
##############################################################################
def access_blocked(html_output_str):
    return ACCESS_BLOCK_SEARCH_STR in html_output_str

def this_is_a_good_html(html_output_str):
    return AR2_SEARCH_STR[0] in html_output_str \
            and AR1_SEARCH_STR[0] in html_output_str \
            and HAKEM_SEARCH_STR[0] in html_output_str \
            and AWAY_TEAM_SEARCH_STR[0] in html_output_str \
            and HOME_TEAM_SEARCH_STR[0] in html_output_str \
            and STAD_SEARCH_STR[0] in html_output_str \
            and MAC_ID_SEARCH_STR in html_output_str \
            and ORGANIZASYON_NAME_SEARCH_STR in html_output_str \
            and DATETIME_SEARCH_STR in html_output_str \
            and HOME_TEAM_SKOR_SEARCH_STR in html_output_str \
            and AWAY_TEAM_SKOR_SEARCH_STR in html_output_str

##############################################################################

def break_down_pattern_one(html_output_str, search_str, end_character):
    # Format: search_str[0] + blablablabla + search_str[1] + ID + "> + NAME + <
    # 18486">BAK TUNCAY AKKIN(1. Yardmc Hakem)<
    # This pattern is very common, break this apart as:
    #       'hakemId='', '18486', 'BAK TUNCAY AKKIN(1. Yardmc Hakem)'

    # Find the first string index
    idx1 = html_output_str.find(search_str[0])
    if idx1 == -1:
        # If the search_str is not contained in the html file, return empty
        return [], ''
    else:
        # Find the second string index after the first one
        idx2 = html_output_str.find(search_str[1], idx1)
        # Reduce the html to a long substring the contains the information
        start_idx = idx2 + len(search_str[1])
        end_idx = idx2 + len(search_str[1]) + SEARCH_MAX
        long_string = html_output_str[start_idx:end_idx]

        # Now, find the information in this long substring
        count = 0
        id_str = ''
        name = ''
        while long_string[count] is not '"':
            id_str = id_str + long_string[count]
            count = count+1
        # Next charachter is '"', the second next must be '>'
        count = count + 1
        if long_string[count] is not '>':
            raise Exception('Something is wrong')
        # Start reading the stad name until '<'
        count = count + 1
        while long_string[count] is not end_character:
            name = name + long_string[count]
            count = count + 1
        # Cleanup extra spaces in the name
        name = ' '.join(name.split())
        return ([], '') if id_str=='' else (int(id_str), name)

def find_dort(html_output_str):
    # 03_lnkHakem" href="Default.aspx?pageId=72&amp;hakemId=19089">TOLGA �ZKALFA(D�rd�nc� Hakem)<
    end_char = '('
    return break_down_pattern_one(html_output_str, DORT_SEARCH_STR, end_char)

def find_ar2(html_output_str):
    # 02_lnkHakem" href="Default.aspx?pageId=72&amp;hakemId=20658">MUSTAFA HELVACIO�LU(2. Yard�mc� Hakem)<
    end_char = '('
    return break_down_pattern_one(html_output_str, AR2_SEARCH_STR, end_char)

def find_ar1(html_output_str):
    # 01_lnkHakem" href="Default.aspx?pageId=72&amp;hakemId=18549">TOLGA KADAZ(1. Yard�mc� Hakem)<
    end_char = '('
    return break_down_pattern_one(html_output_str, AR1_SEARCH_STR, end_char)

def find_hakem(html_output_str):
    # 00_lnkHakem" href="Default.aspx?pageId=72&amp;hakemId=19553">CUMHUR ALTAY(Hakem)<
    end_char = '('
    return break_down_pattern_one(html_output_str, HAKEM_SEARCH_STR, end_char)

def find_away_team(html_output_str):
    # Takim2" href="Default.aspx?pageId=28&amp;kulupId=3590">BE��KTA� A.�.<
    end_char = '<'
    return break_down_pattern_one(html_output_str, \
                                                AWAY_TEAM_SEARCH_STR, end_char)

def find_home_team(html_output_str):
    # Takim1" href="Default.aspx?pageId=28&amp;kulupId=110">VESTEL MAN�SASPOR<
    end_char = '<'
    return break_down_pattern_one(html_output_str, \
                                                HOME_TEAM_SEARCH_STR, end_char)

def find_stad(html_output_str):
    # stadId=11">ANKARA 19 MAYIS<
    end_char = '<'
    return break_down_pattern_one(html_output_str, STAD_SEARCH_STR, end_char)

###############################################################################

def break_down_pattern_two(html_output_str, search_str, end_character):
    # MacBilgisi_lblOrganizasyonAdi">Paf Ligi (PAF Tak�m�) <
    # MacBilgisi_lblTarih">6.08.2006 - 17:00<
    # Goal: Get the part in between >< as a string
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

def find_mac_id(html_output_str):
    # ;macId=15"
    end_char = '"'
    return int(break_down_pattern_two(html_output_str, \
                                                MAC_ID_SEARCH_STR, end_char))

def find_organizasyon_name(html_output_str):
    # MacBilgisi_lblOrganizasyonAdi">Paf Ligi (PAF Tak�m�) <
    end_char = '<'
    organizasyon_name = break_down_pattern_two(html_output_str, \
                                        ORGANIZASYON_NAME_SEARCH_STR, end_char)
    if organizasyon_name[-1] == ' ':
        return organizasyon_name[0:-1]
    else:
        return organizasyon_name

def find_datetime(html_output_str):
    # MacBilgisi_lblTarih">6.08.2006 - 17:00<
    end_char = '<'
    datetime_str = break_down_pattern_two(html_output_str, \
                                                DATETIME_SEARCH_STR, end_char)
    if ':' in datetime_str:
        # Note: Applies to almost all matches
        # Split using '.' to get day and month
        x = datetime_str.split('.')
        day_str, month_str = x[0], x[1]
        # Split the last part using ' - ' to get year
        y = x[-1].split(' - ')
        year_str = y[0]
        # Split the last part using ':' to get hour and minute
        hour_str, minute_str = y[-1].split(':')
    else:
        # EXCEPTION
        # NO TIME: http://www.tff.org/Default.aspx?pageID=29&macId=49400
        x = datetime_str.split('.')
        day_str, month_str, year_str = x[0], x[1], x[2]
        hour_str, minute_str = 12, 0 # Assume match is at noon

    return datetime.datetime(int(year_str), int(month_str), int(day_str),\
                                            int(hour_str), int(minute_str))

def find_home_team_skor(html_output_str):
    # Takim1Skor">1<
    end_char = '<'
    # Exception: No score, such as Takim1Skor"><
    skor = break_down_pattern_two(html_output_str, \
                                            HOME_TEAM_SKOR_SEARCH_STR, end_char)
    return int(skor) if skor is not '' else -1

def find_away_team_skor(html_output_str):
    # Label12">1<
    end_char = '<'
    # Exception: No score, such as Takim1Skor"><
    skor_str = break_down_pattern_two(html_output_str, \
                                            AWAY_TEAM_SKOR_SEARCH_STR, end_char)
    return int(skor_str) if skor_str is not '' else -1
