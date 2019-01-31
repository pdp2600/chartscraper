# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 18:33:52 2019
Example driver script for ChartScraper.py
@author: PDP2600
"""
import pandas as pd
import numpy as np
#Setup a symlink to the site-packages folder, to the drive I do work on and 
#created a folder called local_modules to store my personal/local modules
from local_modules import ChartScraper as cs

#import os
#import sys
#sys.path.append('D:\\Libraries\\Documents\\local_python_modules')
#os.chdir("D:\\Libraries\\Documents\\Python Scripts\\Billboard_Chart_Scraper")
#import ChartScraper as cs

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

dir_path = "D:\\Libraries\\Documents\\Python Scripts\\Billboard_Chart_Scraper"
csv_path = dir_path + "\\ChartScraper_data\\"

##Debugging lines
test_file_content = open('Hip-Hop_Song_Chart_content_1977-01-03.txt', 'w')
#test_file_content_2 = open('URLs_Rumors_bb_mail.txt', 'w')

test_chart = cs.requests.get('https://www.billboard.com/charts/r-b-hip-hop-songs/1977-01-03')
##Remove \n from the content text, it won't serve any purpose and will only get in the way
test_chart_str = str(test_chart.content).replace('\\n', '')

test_file_content.write(str(test_chart.content))
#test_file_content_2.write(str(urls_for_email))
test_file_content.close()
#test_file_content_2.close()
str(test_chart.content).index('<div class="chart-number-one__last-week">')
str(test_chart.content).index('<div class="chart-details ">')
#test_chart_rest = test_chart_str[test_chart_str.index('data-rank'):test_chart_str.index('</main>')]
#chart_list = test_chart_rest.split(sep='<div class="chart-list-item  " data-rank=')


#####################################
#hip_hop_albums = bb_get_multiple_charts('r-b-hip-hop-albums', '1977-01-08', '2018-11-18')
#hip_hop_songs_test = cs.bb_get_multiple_charts('r-b-hip-hop-songs', '1978-11-11', '1978-11-27')
#hip_hop_albums.to_csv('2018-11-19_Hip_Hop_Albums_from_1977-01-08.csv')
#hip_hop_songs.to_csv('2018-11-19_Hip_Hop_Songs_from_1977-01-08.csv')

#hip_hop_songs_test = cs.bb_get_multiple_charts('r-b-hip-hop-songs', '1958-10-20', '1978-11-30')

##Number 1 song "RUmors" has no artist (and doesn't seem to have one in other weekly charts not #1)
##Artist I think is "Timex Social Club"
##May need to update the rest of chart extractor too
###Fix with this #hip_hop_songs.artist = np.where(hip_hop_songs['artist'] == '===<Missing_Artist>===', 'Timex Social Club', hip_hop_songs.artist)

########
hip_hop_albums = cs.bb_get_multiple_charts('r-b-hip-hop-albums', '1965-01-30', '2018-12-31')
#Entries were missing an artist for one title, determined it was likely Kenny G
hip_hop_albums.artist = np.where(hip_hop_albums['artist'] == '===<Missing_Artist>===', 'Kenny G', hip_hop_albums.artist)
hip_hop_albums.to_csv(csv_path + 'All_Hip_Hop_Albums_from_1965-01-30_to_2018-12-31.csv')
hip_hop_songs_part_1 = cs.bb_get_multiple_charts('r-b-hip-hop-songs', '1958-10-20', '1978-11-11')
#There's a weird gap in the weekly charts from 1978-11-12 - 1978-11-14
#Skipping chart for 1978-11-13 as atm it's only displaying the #1
hip_hop_songs_part_1_B = cs.bb_get_weekly_chart('r-b-hip-hop-songs', '1978-11-11')
hip_hop_songs_part_1_B = cs._bb_format_columns(hip_hop_songs_part_1_B)
hip_hop_songs_part_1 = hip_hop_songs_part_1.append(hip_hop_songs_part_1_B)
hip_hop_songs_part_2 = cs.bb_get_multiple_charts('r-b-hip-hop-songs', '1978-11-18', '2018-12-31')
hip_hop_songs = hip_hop_songs_part_1.append(hip_hop_songs_part_2)
#Entries were missing an artist for one title, determined it was likely Timex Social Club
hip_hop_songs.artist = np.where(hip_hop_songs['artist'] == '===<Missing_Artist>===', 'Timex Social Club', hip_hop_songs.artist)
hip_hop_songs.to_csv(csv_path + 'All_Hip_Hop_Songs_from_1958-10-20_to_2018-12-31.csv')
hot_100 = cs.bb_get_multiple_charts('hot-100', '1958-08-04', '1979-12-31')
hot_100_2 = cs.bb_get_multiple_charts('hot-100', '1980-01-06', '1999-12-31')
hot_100 = hot_100.append(hot_100_2)
hot_100_3 = cs.bb_get_multiple_charts('hot-100', '2000-01-07', '2018-12-31')
hot_100 = hot_100.append(hot_100_3)
hot_100.to_csv(csv_path + 'All_Hot_100_from_1958-08-04_to_2018-12-31.csv')
bb_200 = cs.bb_get_multiple_charts('billboard-200', '1963-08-17', '2018-12-31')
#Missing artist for album Silhouette appears to be by Kenny G
bb_200.artist = np.where(bb_200['title'] == 'Silhouette', 'Kenny G', bb_200.artist)
#Missing artist for album Roots of Country Music (1965) appears to be by Various Artsts
bb_200.artist = np.where(bb_200['title'] == 'Roots Of Country Music (1965)', 
                         'Various Artists', bb_200.artist)
bb_200.to_csv(csv_path + 'All_Billboard_200_from_1963-08-17_to_2018-12-31.csv')
##Resume here
pop_songs = cs.bb_get_multiple_charts('pop-songs', '1992-10-03', '2018-12-31')
pop_songs.to_csv(csv_path + 'All_Pop_Songs_from_1992-10-03_to_2018-12-31.csv')
rock_songs = cs.bb_get_multiple_charts('rock-songs', '2009-06-20', '2018-12-31')
rock_songs.to_csv(csv_path + 'All_Rock_Songs_from_2009-06-20_to_2018-12-31.csv')
latin_songs = cs.bb_get_multiple_charts('latin-songs', '1986-09-20', '2018-12-31')
latin_songs.to_csv(csv_path + 'All_Latin_Songs_from_1986-09-20_to_2018-12-31.csv') 
dance_elec_songs = cs.bb_get_multiple_charts('dance-electronic-songs', '2013-01-26', '2018-12-31')
dance_elec_songs.to_csv(csv_path + 'All_Dance_Electronic_Songs_from_2013-01-26_to_2018-12-31.csv')
youtube_chart = cs.bb_get_multiple_charts('youtube', '2011-08-27', '2018-12-31')
youtube_chart.to_csv(csv_path + 'All_YouTube_chart_from_2011-08-27_to_2018-12-31.csv')
japan_hot_100 = cs.bb_get_multiple_charts('japan-hot-100', '2011-04-09', '2018-12-31')
japan_hot_100.to_csv(csv_path + 'All_Japan_Hot_100_from_2011-04-09_to_2018-12-31.csv')
country_songs = cs.bb_get_multiple_charts('country-songs', '1958-10-20', '2018-12-31')
country_songs.to_csv(csv_path + 'All_Country_Songs_from_2011-04-09_to_2018-12-31.csv')