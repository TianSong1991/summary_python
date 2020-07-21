#抓取MiuMiu微博所有评论
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd



def switch_to_window():
    nowhandle=driver.current_window_handle

    allhandles=driver.window_handles

    for handle in allhandles:
        if handle != nowhandle:
            driver.switch_to_window(handle)

def use_mouse_add_hide_content():
    for i in range(5):
        driver.execute_script('window.scrollTo(0,1000000)')
        time.sleep(5)

def get_comment_time():
    for i in range(50):
        try:
            element = driver.find_element_by_class_name("more_txt")
            driver.find_element_by_class_name("more_txt").click()
            time.sleep(8)
        except NoSuchElementException as e:
            print(e)
            break

def write_to_txt(commentdata_1,timedata):
    for i in range(len(commentdata_1)):
        with open('D:\\comment_time.txt',mode='a+',encoding='utf-8') as f:#数据保存地址
            f.write(commentdata_1.iloc[i,0])
            f.write('\t')
            f.write(timedata[i+1].text)
            f.write('\n') 

def get_one_page()
    for num in range(2,47):
        print("The {} comment is start!".format(num))
        #use_mouse_add_hide_content()
        if driver.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div['+str(num)+']/div[2]/div/ul/li[3]/a/span/span/span/em[2]').text == '评论':
            continue
        driver.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div['+str(num)+']/div[1]/div[3]/div[2]/a[1]').click()
        time.sleep(5)
        switch_to_window()

        use_mouse_add_hide_content()

        get_comment_time()

        commentdata = driver.find_elements_by_class_name("WB_text")
        timedata = driver.find_elements_by_css_selector("[class='WB_from S_txt2']")
        commentdata_1 = pd.DataFrame([commentdata[1].text],columns=["text"])
        for i in range(2,len(commentdata)):
            commentdata_2 = pd.DataFrame([commentdata[i].text],columns=["text"])
            if '：' in commentdata_2["text"][0]:
                commentdata_1 = pd.concat((commentdata_1,commentdata_2))

        write_to_txt(commentdata_1,timedata)

        driver.close()
        allhandles=driver.window_handles
        for handle in allhandles:
            driver.switch_to_window(handle)
        time.sleep(5)
    

if __name__ == '__main__':
    driver = webdriver.Chrome()

    driver.get('https://weibo.com')

    driver.find_element_by_id('loginname').send_keys('******')

    driver.find_element_by_name('password').send_keys('******')

    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    time.sleep(10)

    driver.get('https://weibo.com/miumiuofficial?profile_ftype=1&is_all=1#_0')
    for j in range(29):
        get_one_page()
        driver.find_element_by_link_text('下一页').click()
        time.sleep(10)