#!/usr/bin/#!/usr/bin/env python3

import match_info_extractor as mie
import TFF_match
import datetime

### ADD A TEST FOR DORDUNCU HAKEM

SAMPLE_MATCH_OUTPUT = ['sample_TFF_match_html_output_1.txt', \
                       'sample_TFF_match_html_output_2.txt', \
                       'sample_TFF_match_html_output_2.txt']

mac_id = [2, 15, 15]
stad_id = [11, 141, 141]
stad_name = ['ANKARA 19 MAYIS', '8 EYL�L SUN� ��M', '8 EYL�L SUN� ��M']
hakem_id = [18626, 19553, 19553]
hakem_name = ['C�NEYT �AKIR', 'CUMHUR ALTAY', 'CUMHUR ALTAY']
ar1_id = [18486, 18549, 18549]
ar1_name = ['BAK� TUNCAY AKKIN', 'TOLGA KADAZ', 'TOLGA KADAZ']
ar2_id = [18638, 20658, 20658]
ar2_name = ['ALPASLAN DEDE�', 'MUSTAFA HELVACIO�LU', 'MUSTAFA HELVACIO�LU']
dort_id = [19089,[],[]]
dort_name = ['TOLGA �ZKALFA', '', '']
mac_datetime = [datetime.datetime(2006, 8, 4, 21, 0), \
                datetime.datetime(2006, 8, 6, 17, 0), \
                datetime.datetime(2006, 8, 6, 17, 0)]
mac_organizasyon_name = ['Turkcell S�per Lig (Profesyonel Tak�m)', \
                        'Paf Ligi (PAF Tak�m�)', \
                        'Paf Ligi (PAF Tak�m�)']
home_team_id = [4355, 110, 110]
home_team_name = ['ANKARASPOR A.�.', 'VESTEL MAN�SASPOR', 'VESTEL MAN�SASPOR']
home_team_skor = [1, 1, 1]
away_team_id = [3604, 3590, 3590]
away_team_name = ['GALATASARAY A.�.', 'BE��KTA� A.�.', 'BE��KTA� A.�.']
away_team_skor = [1, 1, 1]

def read_and_assert(sample_match_outputs, func_handle, manual_input_data):
    for i in range(len(sample_match_outputs)):
        with open(sample_match_outputs[i], 'r') as sample_file:
            if len(manual_input_data) == len(sample_match_outputs):
                assert func_handle(sample_file.read()) == manual_input_data[i]
            elif len(manual_input_data) == 2:
                assert func_handle(sample_file.read()) == \
                (manual_input_data[0][i], manual_input_data[1][i])

def test_find_mac_id():
    read_and_assert(SAMPLE_MATCH_OUTPUT, mie.find_mac_id, mac_id)

def test_find_stad():
    read_and_assert(SAMPLE_MATCH_OUTPUT, mie.find_stad, [stad_id, stad_name])

def test_find_hakem():
    read_and_assert(SAMPLE_MATCH_OUTPUT, mie.find_hakem, [hakem_id, hakem_name])

def test_find_ar1():
    read_and_assert(SAMPLE_MATCH_OUTPUT, mie.find_ar1, [ar1_id, ar1_name])

def test_find_ar2():
    read_and_assert(SAMPLE_MATCH_OUTPUT, mie.find_ar2, [ar2_id, ar2_name])

def test_find_dort():
    read_and_assert(SAMPLE_MATCH_OUTPUT, mie.find_dort, [dort_id, dort_name])

def test_find_datetime():
    read_and_assert(SAMPLE_MATCH_OUTPUT, mie.find_datetime, mac_datetime)

def test_find_organizasyon_name():
    read_and_assert(SAMPLE_MATCH_OUTPUT, \
                        mie.find_organizasyon_name, mac_organizasyon_name)

def test_find_home_team():
    read_and_assert(SAMPLE_MATCH_OUTPUT, \
                        mie.find_home_team, [home_team_id, home_team_name])

def test_find_home_team_skor():
    read_and_assert(SAMPLE_MATCH_OUTPUT, \
                        mie.find_home_team_skor, home_team_skor)

def test_find_away_team():
    read_and_assert(SAMPLE_MATCH_OUTPUT, \
                        mie.find_away_team, [away_team_id, away_team_name])

def test_find_away_team_skor():
    read_and_assert(SAMPLE_MATCH_OUTPUT, \
                        mie.find_away_team_skor, away_team_skor)
