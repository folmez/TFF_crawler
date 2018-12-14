import datetime
import sys

SEARCH_MAX = 100

# These search strings are assumed to appear at least once, and have identical
# information no matter how many times they appear
DORT_SEARCH_STR = ['03_lnkHakem', 'hakemId=']
AR2_SEARCH_STR = ['02_lnkHakem', 'hakemId=']
AR1_SEARCH_STR = ['01_lnkHakem', 'hakemId=']
HAKEM_SEARCH_STR = ['00_lnkHakem', 'hakemId=']
AWAY_TEAM_SEARCH_STR = ['Takim2"', 'kulupId=']
HOME_TEAM_SEARCH_STR = ['Takim1"', 'kulupId=']
STAD_SEARCH_STR = ['lnkStad', 'stadId=']

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
