from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import pandas as pd
import os
import time

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

url = "https://www.youtube.com/channel/UChsKg9spb34z_lKZIJLYmeA/videos"

driver.get(url)

scroll_times = (2000 // 30)

for i in range(0, scroll_times):
    height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(3)
    driver.find_element_by_tag_name('body').send_keys(Keys.END)

soup = BeautifulSoup(driver.page_source, 'lxml')

"""
with open('./html_pages/full_page_discovery.html', mode='wt', encoding='utf-8') as file:
    file.write(str(soup.encode('utf-8')))
    file.close()
"""

video_grid = soup.find('div', class_="style-scope ytd-grid-renderer")


thumbnails = video_grid.find_all('img', id='img')
thumbnails_list = []
for thumbnail in thumbnails:
    try:
        thumbnails_list.append(thumbnail['src'])
    except:
        thumbnails_list.append(None)

video_paths = video_grid.find_all('ytd-thumbnail', class_="style-scope ytd-grid-video-renderer")
video_paths_list = []
for path in video_paths:
    try:
        video_paths_list.append(path.a['href'])
    except:
        video_paths_list.append(None)


titles = video_grid.find_all('a', {'id': 'video-title'})
titles_list = []
for title in titles:
    try:
        titles_list.append(title.text)
    except:
        titles_list.append(None)

video_durations = video_grid.find_all('span', class_="style-scope ytd-thumbnail-overlay-time-status-renderer")
video_durations_list = []
for time in video_durations:
    try:
        if time.text:
            video_durations_list.append(time.text)
        else:
            video_durations_list.append(None)
    except:
        video_durations_list.append(None)

video_views_and_date_posted = video_grid.find_all('div', class_="style-scope ytd-grid-video-renderer", id='metadata-line')
video_views_list = []
date_posted_list = []
for item in video_views_and_date_posted:
    try:
        video_views_list.append(item.span.text)
        date_posted_list.append(item.span.next_sibling.next_sibling.text)
    except:
        video_views_list.append(None)
        date_posted_list.append(None)

print('Video URL: ' + str(len(video_paths_list)))
print('Title: ' + str(len(titles_list)))
print('Duration: ' +  str(len(video_durations_list)))
print('Views: ' + str(len(video_views_list)))
print('Date Posted: ' + str(len(date_posted_list)))

df_yt_channel_videos = pd.DataFrame(
    {
        'image': thumbnails_list,
        'video_path': video_paths_list,
        'duration': video_durations_list,
        'title': titles_list,
        'views': video_views_list,
        'date_posted': date_posted_list
    }
)

print(df_yt_channel_videos)

df_yt_channel_videos.to_csv('./output/tlc_sea.csv')