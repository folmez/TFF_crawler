import match_csv_tools

def test_get_header_row():
    assert match_csv_tools.get_header_row() == \
                    ['TFF Match ID', 'Tarih', 'Organizasyon', 'Hakem ID', \
                    'Hakem', 'AR1 ID', 'AR1', 'AR2 ID', 'AR2', 'Dort ID', \
                    'Dorduncu Hakem', 'Stad ID', 'Stad','Ev', 'Ev ID', \
                    'Deplasman', 'Deplasman ID', 'Ev skor', 'Deplasman skor']
