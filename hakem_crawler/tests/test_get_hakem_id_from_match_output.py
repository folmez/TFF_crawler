import hakem_csv_tools as hct

TEST_MATCH_OUTPUT = '/home/folmez/Dropbox/Research1/fun-experiments/TFF_crawler/hakem_crawler/tests/sample_test_files/test_match_output.csv'

def test_get_hakem_id_from_match_output():
    hakem_set = set([17960,17774,20747,19531,18902,19963,20144,19021, \
                    19928,18958,20887,20259,20132,20565,19158,19709, \
                    20291,19521,20442,20294,18870,19973,20799,20113, \
                    19381,19630,20865,20417,19149,19761,20458,19678, \
                    19149,19761,20458])
    assert set(hct.get_hakem_id_from_match_output(TEST_MATCH_OUTPUT)) == hakem_set
