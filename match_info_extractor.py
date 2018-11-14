def find_stad(html_output_str):
    # stadId=11">ANKARA 19 MAYIS<
    search_max = get_max_str_search_length()
    search_str = 'stadId='
    find_count = 0
    while True:
        idx = html_output_str.find(search_str, find_count)
        if idx==-1:
            break
        start_idx = idx + len(search_str)
        end_idx = idx + len(search_str) + search_max
        stad_id, stad_name = break_down_patter(search_str,\
                        html_output_str[start_idx:end_idx])
        find_count = idx + 1
    return stad_id, stad_name

def find_hakemler(html_output_str):
    # The string 'hakemId=' seems to appear four times
    search_max = get_max_str_search_length()
    search_str = 'hakemId='
    hakem_ids = []
    hakem_names = []
    find_count = 0
    while True:
        idx = html_output_str.find(search_str, find_count)
        if idx==-1:
            break
        start_idx = idx + len(search_str)
        end_idx = idx + len(search_str) + search_max
        i, n = break_down_patter(search_str,\
                        html_output_str[start_idx:end_idx])
        hakem_ids.append(i)
        hakem_names.append(n)
        find_count = idx + 1
    return hakem_ids, hakem_names

def break_down_patter(init_subtring, long_string):
    # 18486">BAK TUNCAY AKKIN(1. Yardmc Hakem)</a></div>\r\n
    # This pattern is very common, break this apart as:
    #       'hakemId='', '18486', 'BAK TUNCAY AKKIN(1. Yardmc Hakem)'
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
    while long_string[count] is not '<':
        name = name + long_string[count]
        count = count + 1
    return int(id_str), name

def get_max_str_search_length():
    return 50
