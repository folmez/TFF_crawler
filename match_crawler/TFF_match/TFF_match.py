#!/usr/bin/#!/usr/bin/env python3

import match_info_extractor_tools as mie

class match:
    def __init__(self, html_output_str):
        self.mac_id = mie.find_mac_id(html_output_str)
        self.stad_id, self.stad_name = mie.find_stad(html_output_str)

        self.hakem_id, self.hakem_name = mie.find_hakem(html_output_str)
        self.ar1_id, self.ar1_name = mie.find_ar1(html_output_str)
        self.ar2_id, self.ar2_name = mie.find_ar2(html_output_str)
        self.dort_id, self.dort_name = mie.find_dort(html_output_str)

        self.datetime = mie.find_datetime(html_output_str)
        self.organizasyon_name = mie.find_organizasyon_name(html_output_str)

        self.home_team_id, self.home_team_name = mie.find_home_team(html_output_str)
        self.away_team_id, self.away_team_name = mie.find_away_team(html_output_str)

        self.home_team_skor = mie.find_home_team_skor(html_output_str)
        self.away_team_skor = mie.find_away_team_skor(html_output_str)

    def all_info_in_one_line(self):
        # backup = f"{self.mac_id},{self.datetime},{self.organizasyon_name},{self.hakem_id},{self.hakem_name},{self.ar1_id},{self.ar1_name},{self.ar2_id},{self.ar2_name},{self.dort_id},{self.dort_name},{self.stad_id},{self.stad_name},{self.home_team_id},{self.home_team_name},{self.away_team_id},{self.away_team_name},{self.home_team_skor},{self.away_team_skor}"
        return str(self.mac_id) + ',' + str(self.datetime) + ',' + \
                self.organizasyon_name + ',' + \
                str(self.hakem_id) + ',' + self.hakem_name + ',' + \
                str(self.ar1_id) + ',' + self.ar1_name + ',' + \
                str(self.ar2_id) + ',' + self.ar2_name + ',' + \
                str(self.dort_id) + ',' + self.dort_name + ',' + \
                str(self.stad_id) + ',' + self.stad_name + ',' + \
                str(self.home_team_id) + ',' + self.home_team_name + ',' + \
                str(self.away_team_id) + ',' + self.away_team_name + ',' + \
                str(self.home_team_skor) + ',' + str(self.away_team_skor)

    def print_summary(self, silent):
        header = '[' + 'TFF match #' + str(self.mac_id) + ']'
        if not silent:
            print(header, self.datetime)
            print(header, self.hakem_name, ',', \
                            self.ar1_name, ',', self.ar2_name, ',', self.dort_name)
            print(header, self.home_team_name, self.home_team_skor, '-', \
                            self.away_team_skor, self.away_team_name)
