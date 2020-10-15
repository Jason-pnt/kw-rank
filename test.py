# -*- coding: utf-8 -*-
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
#pip3 install pillow selenium pytz
import xlrd
import openpyxl
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert 
from PIL import Image
import time
import csv
import re
import sys
import datetime
import string
import os
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--disable-images')
chrome_options.add_argument('--start-maximized')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://tools.keycdn.com/geo')
cityName = (driver.find_element_by_xpath('//*[@id="geoResult"]/div[1]/dl[1]/dd[1]').text)
zipcode = (driver.find_element_by_xpath('//*[@id="geoResult"]/div[1]/dl[1]/dd[3]').text)
country = (driver.find_element_by_xpath('//*[@id="geoResult"]/div[1]/dl[1]/dd[4]').text)
print('\n\nNow test begining country: ' + country + ' city: ' + cityName + ' Zipcode: '+ zipcode + '\n\n')

driver.get('https://www.amazon.com/?currency=USD&language=en_US')
time.sleep(5)
driver.find_element_by_xpath('//*[@id="nav-packard-glow-loc-icon"]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys('10001')
time.sleep(5)
driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input').click()
time.sleep(5)
driver.get('https://www.amazon.com/')
print('\n Amazon ZIPCode:'+ driver.find_element_by_xpath('//*[@id="glow-ingress-line2"]').text)

counts = 0
final_result = {}

data = xlrd.open_workbook('test.xlsx')
data.sheet_names()
ASIN = ''.join(data.sheet_names())
table = data.sheet_by_index(0)
col1 = (table.col_values(0))
print("总行数：" + str(table.nrows))
print("总列数：" + str(table.ncols))
print('asin is :' + ASIN)
for i in range(len(col1)):
    col1[i] = str(col1[i]).strip()

diff = []

for i in col1:
    if (len(i) != 0):
        lineToList = i.split(' ')
        linkStr='s?k='
        for a in range(len(lineToList)):
            linkStr = linkStr +lineToList[a] + '+'
        linkStr[:-1]
        counts = 1 + counts
        driver.maximize_window()
        flags = False
        keyword = linkStr.replace('+', ' ')[4:]
        print(str(counts) + ' for  keyword: ' + keyword)
        if (keyword not in final_result):
            final_result[keyword] = [0,0,0]
        for i in range(1,7):
            if (final_result[keyword][1] != 0 and final_result[keyword][2] != 0):
                break
            driver.get('https://www.amazon.com/' + linkStr + '&page=' + str(i)+ '&language=en_US')            
            if flags == False:
                count = driver.find_element_by_xpath('//*[@id="search"]/span/div/span/h1/div/div[1]/div/div/span[1]').text
                count = count.split(' ')[-3].replace(',','')
                if final_result[keyword][0] == 0:
                    final_result[keyword][0] = count
                flags = True
            soup = BeautifulSoup(driver.page_source, "html.parser")
            for asin in soup.find_all(href=re.compile(ASIN)):
                links = str(asin.get('href'))
                if (links.startswith('/gp')):
                    if ('sr_1_' in links):
                        adver = links.split('sr_1_')[1].split('_')[0]
                        if final_result[keyword][1] == 0:
                            final_result[keyword][1] = adver
                    else:
                        if final_result[keyword][1] == 0:
                            final_result[keyword][1] = 0
                        print('Error :\n' + links + '\n Please check it')
                else:
                    if ('sr_1_' in links):
                        nature = links.split('sr_1_')[1].split('?')[0]
                        if final_result[keyword][2] == 0:
                            final_result[keyword][2] = nature
                    else:
                        if final_result[keyword][2] == 0:
                            final_result[keyword][2] = 0
                        print('Error :\n' + links + '\n Please check it')
driver.quit()
print("\n\n")
for k,v in final_result.items():
    print('key: ',k,','.join(v))

pf = pd.DataFrame(final_result)
pf = pd.DataFrame(pf.values.T, index= pf.columns, columns=pf.index)
file_path = pd.ExcelWriter('asin-top.xlsx')
pf.to_excel(file_path,encoding='utf-8',index=True)
file_path.save()