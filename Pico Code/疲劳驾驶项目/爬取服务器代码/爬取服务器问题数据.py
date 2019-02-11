import os 
import requests
import re
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs

path1 = 'E:\\Data\\test'
os.chdir(path1)

driver = webdriver.Chrome()
driver.get("http://******")
time.sleep(2)

driver.find_element_by_id("account").send_keys("***")
time.sleep(1)
driver.find_element_by_id("password").send_keys("***")
time.sleep(1)
driver.find_element_by_id("loginBtn").click()
time.sleep(1)


driver.find_element_by_link_text("我的驾驶").click()
time.sleep(1)
driver.find_element_by_link_text("疲劳数据").click()

j = 0

for n in range(250):
	content1 = driver.page_source

	content2 = bs(content1,'lxml')

	for i in content2.findAll('a',class_="image-zoom"):
	    print(i['href'])
	    response = requests.get(i['href'])
	    img = response.content
	    j = j + 1
	    with open( str(j)+'.jpg','wb' ) as f:
	        f.write(img)

	time.sleep(2)

	driver.find_element_by_xpath('//*[@id="pageContainer"]/nav/ul/li[8]/a/span').click()#点击进入下一页

	time.sleep(3)



