import match_info_extractor_tools as mie

def test_import_MAC_ID_SEARCH_STR():
    assert mie.MAC_ID_SEARCH_STR == ';macId='

def test_import_ORGANIZASYON_NAME_SEARCH_STR():
            mie.ORGANIZASYON_NAME_SEARCH_STR == 'MacBilgisi_lblOrganizasyonAdi">'

def test_import_DATETIME_SEARCH_STR():
            mie.DATETIME_SEARCH_STR == 'MacBilgisi_lblTarih">'

def test_import_HOME_TEAM_SKOR_SEARCH_STR():
            mie.HOME_TEAM_SKOR_SEARCH_STR == 'Takim1Skor">'

def test_import_AWAY_TEAM_SKOR_SEARCH_STR():
            mie.AWAY_TEAM_SKOR_SEARCH_STR == 'Label12">'

def test_import_DORT_SEARCH_STR():
            mie.DORT_SEARCH_STR == ['03_lnkHakem', 'hakemId=']

def test_import_AR2_SEARCH_STR():
            mie.AR2_SEARCH_STR == ['02_lnkHakem', 'hakemId=']

def test_import_AR1_SEARCH_STR():
            mie.AR1_SEARCH_STR == ['01_lnkHakem', 'hakemId=']

def test_import_HAKEM_SEARCH_STR():
            mie.HAKEM_SEARCH_STR == ['00_lnkHakem', 'hakemId=']

def test_import_AWAY_TEAM_SEARCH_STR():
            mie.AWAY_TEAM_SEARCH_STR == ['Takim2"', 'kulupId=']

def test_import_HOME_TEAM_SEARCH_STR():
            mie.HOME_TEAM_SEARCH_STR == ['Takim1"', 'kulupId=']

def test_import_STAD_SEARCH_STR():
            mie.STAD_SEARCH_STR == ['lnkStad', 'stadId=']
