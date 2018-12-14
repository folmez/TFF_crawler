import csv

def get_header_row():
    return ['Name', 'Occupation', 'Lisans', 'Klasman', 'Area']

def get_hakem_id_from_match_output(match_output_filename):
    with open(match_output_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)

        # initialize hakem IDs (not license, database IDs = web-URLs) as a set
        hakem_ids = set()

        # skip the header
        headers = next(csv_reader)

        # get all hakem
        for row in csv_reader:
            for index in [3,5,7,9]: # hakem, AR1, AR2, Dort
                if row[index+1] is not '':
                    hakem_ids.add(int(row[index]))

        print('Number of all referees:', len(hakem_ids))

        return list(hakem_ids)
