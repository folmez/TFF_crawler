import hakem_info_extractor as hie

FOLDERNAME = '/home/folmez/Dropbox/Research1/fun-experiments/TFF_crawler/hakem_crawler/tests/sample_test_files/'
FILENAMES = ['cuneyt_cakir.txt', 'fatih_olmez.txt']
SAMPLE_FILES = [FOLDERNAME + filename for filename in FILENAMES]

def read_and_assert(func_handle, filenames, targets):
    for filename, target in zip(filenames, targets):
        with open(filename, 'r') as f:
            hakem_output_html = f.read()
            assert func_handle(hakem_output_html) == target

def test_find_name():
    read_and_assert(hie.find_name, SAMPLE_FILES, ['CÜNEYT ÇAKIR', 'FATİH ÖLMEZ'])

def test_find_occupation():
    read_and_assert(hie.find_occupation, SAMPLE_FILES, ['İşletmeci', 'Öğrenci'])

def test_lisans_number():
    read_and_assert(hie.find_lisans_number, SAMPLE_FILES, [11750, 29864])

def test_klasman():
    read_and_assert(hie.find_klasman, SAMPLE_FILES, ['Süper Lig Hakemi', 'İl Hakemi'])

def test_area():
    read_and_assert(hie.find_area, SAMPLE_FILES, ['İSTANBUL', 'İSTANBUL'])
