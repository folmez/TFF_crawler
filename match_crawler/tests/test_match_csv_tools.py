import match_csv_tools

def test_get_header_row():
    assert match_csv_tools.get_header_row() == \
                    ['TFF Match ID', 'Tarih', 'Organizasyon', 'Hakem ID', \
                    'Hakem', 'AR1 ID', 'AR1', 'AR2 ID', 'AR2', 'Dort ID', \
                    'Dorduncu Hakem', 'Stad ID', 'Stad','Ev', 'Ev ID', \
                    'Deplasman', 'Deplasman ID', 'Ev skor', 'Deplasman skor']

def test_get_missing_match_ids_in_range():
    filename = 'tests/sample_test_files/sample_match_output_file.csv'
    assert match_csv_tools.get_missing_match_ids_in_range(1,20,filename) == \
                            [1, 3, 6, 7, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20]
