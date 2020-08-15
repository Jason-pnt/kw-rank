#-*-coding: utf-8 -*-
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
#pip3 install pillow selenium
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
driver.find_element_by_xpath('//*[@id="nav-packard-glow-loc-icon"]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="GLUXZipUpdateInput"]').send_keys('10001')
time.sleep(5)
driver.find_element_by_xpath('//*[@id="GLUXZipUpdate"]/span/input').click()
time.sleep(5)
driver.get('https://www.amazon.com/')
print('Amazon ZIPCode:'+ driver.find_element_by_xpath('//*[@id="glow-ingress-line2"]').text)

counts = 0
final_result = {}
with open('test.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        if (len(row) != 0):
            lineToStr = row[0]
            lineToList = lineToStr.split(' ')
            linkStr='s?k='
            for i in range(len(lineToList)):
                linkStr= linkStr + lineToList[i] + '+'
                # picPath = picPath + lineToList[i] +'_'
            linkStr= linkStr[:-1]
            # picPath = picPath[:-1].replace('/','-')
            driver.maximize_window()
            counts = 1 + counts
            flags = False
            keyword = linkStr.replace('+', ' ')[4:]
            print(str(counts) + ' for  keyword: ' + keyword)
            if (keyword not in final_result):
                final_result[keyword] = [0, 0, 0]
            for i in range(1,2):
                # print('page :' + str(i))
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
                for asin in soup.find_all(href=re.compile("READY-PARD-")):
                    links = str(asin.get('href'))
                    print(links)
                    if (links.startswith('/gp')):
                        # adver 
                        adver = links.split('sr_1_')[1].split('_')[0]
                        if final_result[keyword][1] == 0:
                            final_result[keyword][1] = adver
                    else:
                        nature = links.split('sr_1_')[1].split('?')[0]
                        # nature
                        if final_result[keyword][2] == 0:
                            final_result[keyword][2] = nature
driver.quit()
print("\n\n")
for k,v in final_result.items():
    print(k,v)

pf = pd.DataFrame(final_result)
pf = pd.DataFrame(pf.values.T, index= pf.columns, columns=pf.index)
file_path = pd.ExcelWriter('asin-top.xlsx')
pf.to_excel(file_path,encoding='utf-8',index=True)
file_path.save()
