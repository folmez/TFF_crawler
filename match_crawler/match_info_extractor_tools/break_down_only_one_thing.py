import datetime
import sys

SEARCH_MAX = 100

# These search strings are assumed to appear at least once, and have identical
# information no matter how many times they appear
MAC_ID_SEARCH_STR = ';macId='
ORGANIZASYON_NAME_SEARCH_STR = 'MacBilgisi_lblOrganizasyonAdi">'
DATETIME_SEARCH_STR = 'MacBilgisi_lblTarih">'
HOME_TEAM_SKOR_SEARCH_STR = 'Takim1Skor">'
AWAY_TEAM_SKOR_SEARCH_STR = 'Label12">'

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
