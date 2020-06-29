from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import pandas as pd
import os
import time

df = pd.read_csv('yt_crawl_list.csv')
url_list = df['Link']
channel_name = df['Name']

for url in range(0, len(url_list)):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    channel_url = url_list[url]
    driver.get(channel_url)

    scroll_times = (3022 // 30) + 2

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
            print(thumbnail['src'])
            thumbnails_list.append(thumbnail['src'])
        except:
            thumbnails_list.append(None)
            print("No Image Found")

    video_paths = video_grid.find_all('ytd-thumbnail', class_="style-scope ytd-grid-video-renderer")
    video_paths_list = []
    for path in video_paths:
        video_paths_list.append(path.a['href'])


    titles = video_grid.find_all('a', {'id': 'video-title'})
    titles_list = []
    for title in titles:
        titles_list.append(title.text)

    video_durations = video_grid.find_all('span', class_="style-scope ytd-thumbnail-overlay-time-status-renderer")
    video_durations_list = []
    for time in video_durations:
        video_durations_list.append(time.text)

    video_views_and_date_posted = video_grid.find_all('div', class_="style-scope ytd-grid-video-renderer", id='metadata-line')
    video_views_list = []
    date_posted_list = []
    for item in video_views_and_date_posted:
        video_views_list.append(item.span.text)
        date_posted_list.append(item.span.next_sibling.next_sibling.text)


    print(len(thumbnails))
    print(len(video_paths_list))
    print(len(titles_list))
    print(len(video_durations_list))
    print(len(video_views_list))


    df_yt_channel_videos = pd.DataFrame(
        {
            'image': thumbnails_list,
            'video_path': video_paths_list,
            'title': titles_list,
            'duration': video_durations_list,
            'views': video_views_list,
            'date_posted': date_posted_list
        }
    )

    print(df_yt_channel_videos)

    df_yt_channel_videos.to_csv('./output/' + str(i) + '.csv')