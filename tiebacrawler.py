# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import numpy as np

# 定义一个taobao类
class tieba_infos:

    # 对象初始化
    def __init__(self):
        url = 'https://tieba.baidu.com/'
        self.url = url

        options = webdriver.ChromeOptions()
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    # 延时操作,并可选择是否弹出窗口提示
    def sleep_and_alert(self, sec, message, is_alert):

        for second in range(sec):
            if (is_alert):
                alert = "alert(\"" + message + ":" + str(sec - second) + "秒\")"
                self.browser.execute_script(alert)
                al = self.browser.switch_to.alert
                sleep(1)
                al.accept()
            else:
                sleep(1)

    # 第一层爬取，获取主要信息及其连接
    def search_main(self):
        self.browser.get(self.url)
        #登陆界面
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tang-pass-footerBar")))
        self.browser.find_element_by_class_name("tang-pass-footerBarULogin").click()    #点击用户名登陆按钮
        WebDriverWait(self.browser, 10).until(EC.presence_of_all_elements_located)
        self.browser.find_element_by_id("TANGRAM__PSP_4__userName").clear()                     #自动输入用户名
        self.browser.find_element_by_id("TANGRAM__PSP_4__userName").send_keys(tieba_username)
        self.browser.find_element_by_id("TANGRAM__PSP_4__password").clear()                     #自动输入密码
        self.browser.find_element_by_id("TANGRAM__PSP_4__password").send_keys(tieba_password)
        self.browser.find_element_by_id("TANGRAM__PSP_4__submit").click()                       #点击登陆按钮

        #中间会跳出一个旋转图片的人工智能识别，爬虫无法自动实现智能手动旋转

        #贴吧主页
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "wd1")))   #等待搜索框出现
        self.browser.find_element_by_id("wd1").clear()   # 清空里面已有的输入
        self.browser.find_element_by_id("wd1").send_keys("英雄联盟")   # 在里面输入英雄联盟搜索词
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search_form")))   #等待搜索按钮出现
        self.browser.find_element_by_class_name("search_btn_wrap").click()  # 点击搜索按钮

        #进入英雄联盟吧
        tiezi = []      #创建帖子列表
        i = 1
        while(i <= 6):  #爬取前6页的帖子，每页50个贴
            sleep(1)    #强制停止1秒，防止被网站识别出是爬虫
            e_item = self.browser.find_elements_by_xpath('//div[@class="t_con cleafix"]')
            for e in e_item:
                tiezi.append([e.find_element_by_tag_name('a').text, e.find_element_by_tag_name('a').get_attribute('href')])     #获取贴名和url
            self.browser.find_element_by_class_name("next").click()     #点击下一页按钮
            i += 1
        tiezi_df = pd.DataFrame(tiezi)
        tiezi_df.to_csv('C:/Users/fader/Desktop/tiezi1.csv', encoding='utf_8_sig')      #导出为csv文件
    #第二层爬取，获取每个帖子的详细信息
    def search_detials(self):
        #读取主要信息并进行一些简单的处理
        detail = []
        tiezi_df = pd.read_csv('C:/Users/fader/Desktop/tiezi1.csv', encoding='utf_8_sig')
        tiezi_df = tiezi_df.drop(0, axis=0).drop(1, axis=0).drop(2, axis=0)
        tiezi_df.columns = ['index', 'title', 'link']
        self.browser.get('https://tieba.baidu.com/p/7346322237')
        sleep(5)
        self.browser.get('https://tieba.baidu.com/p/7346320883')
        sleep(5)
        self.browser.get('https://tieba.baidu.com/p/7339073903')
        sleep(5)
        #进入每个帖子的链接并进行爬虫
        for row in tiezi_df.itertuples(index=True, name='Pandas'):
            if int(getattr(row, 'index')) > 138:
                print(getattr(row, 'title'), getattr(row, 'link'))
                try:
                    self.browser.get(getattr(row, 'link'))
                    page = self.browser.find_element_by_xpath('//li[@class="l_reply_num"]')     #找到总页数方便以后的翻页
                    pagenum = int(page.find_elements_by_tag_name('span')[1].text)
                    #对所有页进行爬取
                    for i in range(pagenum):
                        #强制停止1秒防止网页反爬虫
                        sleep(1)
                        e_name = []
                        #爬取昵称和评论
                        t_item = self.browser.find_elements_by_xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
                        e_item = self.browser.find_elements_by_xpath('//div[@class="d_post_content j_d_post_content "]')
                        for t in t_item:
                            e_name.append(t.find_element_by_class_name("d_name"))
                        for j in range(len(e_item)):
                            #若评论不为空则加入列表
                            if e_item[j].text != '':
                                detail.append([getattr(row, 'title'), pagenum, e_name[j].find_element_by_tag_name('a').text, e_item[j].text])
                                print(getattr(row, 'index'))

                        #在搜索框输入页码进行翻页
                        self.browser.find_element_by_id("jumpPage6").clear()
                        self.browser.find_element_by_id("jumpPage6").send_keys(str(i + 2))
                        self.browser.find_element_by_id("pager_go6").click()
                except:
                    print('帖子已被删除')
                else:
                    continue
        detail_df = pd.DataFrame(detail)
        arr = np.array(detail)
        np.save('C:/Users/fader/Desktop/detail2.npy', arr)
        detail_df.columns = ['title', 'totalpage', 'nickname', 'comment']      #加列名
        detail_df.to_csv('C:/Users/fader/Desktop/detail2.csv', encoding='utf_8_sig')     #导出csv

if __name__ == "__main__":

    chromedriver_path = "/Users/fader/Desktop/chromedriver.exe"  # chromedriver的完整路径地址
    tieba_username = "######"  # 贴吧账号
    tieba_password = "######"  # 贴吧密码

    a = tieba_infos()
    a.search_main()
    a.search_detials()
