import csv

def get_missing_match_ids_in_range(start, stop, filename):
    with open(filename, 'r') as csv_file:
        cvs_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)

        # skip the header
        headers = next(cvs_reader)

        # get existing match ids (first entry, with a quote in the beginnig)
        existing_match_ids =  [int(row[0][1::]) for row in cvs_reader]

        # put existing match ids in a set for faster membership testing
        s = set(existing_match_ids)

        # get missing match ids
        missing_match_ids = [x for x in range(start, stop+1) if x not in s]

        return missing_match_ids
