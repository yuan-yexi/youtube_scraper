import pandas as pd
import numpy as np
import re
import nltk
import datetime

def remove_characters(df):
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    df['title_lower'] = df['title'].str.lower()
    df['title_lower'] = df['title_lower'].str.replace(r"\n", '')
    df['duration'] = df['duration'].str.replace(r"\n", '')
    df['views'] = df['views'].str.replace(r"views", '')
    
# date parse
def date_parse_to_days(df):
    date_posted = df['date_posted'].tolist()
    parsed_dates = []
    for i in range(0, len(date_posted)):
        if date_posted[i][2] == 'y':
            parsed_dates.append(int(date_posted[i][0]) * 365)
        elif date_posted[i][2] == 'w':
            parsed_dates.append(int(date_posted[i][0]) * 7)
        else:
            parsed_dates.append(int(date_posted[i][0]))
    df['days_since_posted'] = parsed_dates

def views_parser(df):
    num_of_views = df['views'].tolist()
    parsed_views = []
    for i in range(0, len(num_of_views)):
        if "K" in num_of_views[i]:
            num = float(num_of_views[i].replace(r"K", '')) * 1000
            parsed_views.append(int(num))
        elif "M" in num_of_views[i]:
            num = float(num_of_views[i].replace(r"M", '')) * 1000000
            parsed_views.append(int(num))
        else:
            num = float(num_of_views[i])
            parsed_views.append(int(num))
    df['views_int'] = parsed_views

def get_mins_seconds(df):
    time_str = df['duration'].tolist()
    duration_sec = []
    for i in range(0, len(time_str)):
        try: 
            m, s = time_str[i].split(':')
            in_seconds = int(m) * 50 + int(s)
            duration_sec.append(in_seconds)
        except:
            h, m, s = time_str[i].split(':')
            in_seconds = int(h) + int(m) * 50 + int(s)
            duration_sec.append(in_seconds)
    
    df['duration_sec'] = duration_sec
    df['duration_min'] = df['duration_sec'] / 60
    df['duration_min'] = df['duration_min'].round(2)

"""
csv_list = [
    '5minscraft', 'aaronandclaire', 'aboardinjapan', 'animalplanet-us', 'AsapSCIENCE', 'asianboss', 'besteverfoodreviewshow',
    'BonAppetitDotCom', 'bravewilderness', 'buzzfeedbringme', 'buzzfeedunsolvednetwork', 'cgpgrey', 'dailydoseoftheinternet',
    'dsc-sea', 'dsc-uk', 'dsc-us', 'eentertainment', 'foodinsider', 'foodnetworktv', 'haertetest', 'hauzztv', 'hayu', 'hgtv-us',
    'historychannel', 'houseandhomevideo', 'hydraulicpresschannel', 'kingofrandom', 'Kurzgesagt', 'markrober', 'mattrisinger',
    'nevertoosmall', 'realstories', 'say-yes-to-the-dress', 'ScienceChannel', 'stephaniesoo', 'tasty', 'thetryguys', 'tlc-uk',
    'tlc-us', 'TravelThirstyBlog', 'truecrimedaily', 'whatsinside']
"""
csv_list = ['tlc_sea', 'investigation_discovery', 'dcode', 'thisoldhouse']

for csv in csv_list:
    df = pd.read_csv("./output/"+csv+".csv")
    remove_characters(df)
    views_parser(df)
    date_parse_to_days(df)
    df.to_csv("./cleaned_output/cleaned_"+csv+".csv", index = False)