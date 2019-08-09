# *第一部分首先要爬取MiuMiu的每一条微博的mid，mid就是每一条微博的唯一标识符，便于后期直接爬取；
#  此次爬取下来的数据是：mid和评论数两个维度，后去需要将没有评论的mid删除，节省爬虫时间。*
#-------------------------------------------------------------------------------------#

#使用selenium模块进行模拟浏览器爬取，在python下直接pip install selenium安装即可；
#另外需要安装chrome或者Firefox浏览器，推荐使用安装chrome浏览器，并且要根据chrome浏览器的相应版本安装chromedriver，
#chromedriver的版本必须要与安装的chrome版本相对应，要不然selenium调浏览器会出错。

from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get('https://weibo.com')
time.sleep(5)

driver.find_element_by_id('loginName').send_keys('******')

driver.find_element_by_id('loginPassword').send_keys('******')

driver.find_element_by_id('loginAction').click()
time.sleep(5)

driver.get('https://weibo.com/miumiuofficial?profile_ftype=1&is_all=1#_0')#此网址为你需要爬取的微博的主页，手动复制添加即可

for j in range(29):
    print(j)
    for i in range(3):
        driver.execute_script('window.scrollTo(0,1000000)')
        time.sleep(10)
    for i in range(2,47):
        test = driver.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div['+str(i)+']/div[1]/div[3]/div[2]/a[1]')
        comment = driver.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div['+str(i)+']/div[2]/div/ul/li[3]/a/span/span/span/em[2]').text
        url_mid = test.get_attribute('name')
        print(i)
        with open('D:\\newmid_MiuMiu.txt',mode='a+') as f:#数据保存地址
            f.write(url_mid)
            f.write('\t')
            f.write(str(comment))
            f.write('\n')
    driver.find_element_by_link_text('下一页').click()
    time.sleep(10)


