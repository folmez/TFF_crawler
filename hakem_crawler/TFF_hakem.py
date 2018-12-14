#!/usr/bin/#!/usr/bin/env python3

import hakem_info_extractor as hie

class hakem:
    def __init__(self, html_output_str, id):
        self.id = id
        self.name = hie.find_name(html_output_str)
        self.occupation = hie.find_occupation(html_output_str)
        self.lisans = hie.find_lisans_number(html_output_str)
        self.klasman = hie.find_klasman(html_output_str)
        self.area = hie.find_area(html_output_str)

    def all_info_in_one_line(self):
        return str(self.id) + ',' + self.name + ',' + self.occupation + ',' + \
                str(self.lisans) + ',' + self.klasman + ',' + self.area

    def print_summary(self, silent):
        header = '[' + 'Hakem #' + str(self.id) + ']'
        if not silent:
            print(header, self.name, '-', self.occupation)
            print(header, str(self.lisans), '-', self.klasman, '-', self.area)
