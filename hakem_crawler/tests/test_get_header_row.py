import hakem_csv_tools

def test_get_header_row():
    assert hakem_csv_tools.get_header_row() == ['Name', 'Occupation', 'Lisans', 'Klasman', 'Area']
