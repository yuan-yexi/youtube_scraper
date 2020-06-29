from bs4 import BeautifulSoup
import pandas as pd
import os
import time

url = "https://www.youtube.com/user/vice/videos"

soup = BeautifulSoup(driver.page_source, 'lxml')