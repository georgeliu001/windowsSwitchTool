#!/usr/bin/python3
# coding: utf8

import time
from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

driver = None

def waitFor(locator):
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(locator)
    )


# 公司部署的 NanGBS-南宙视频监管系统
class VideoEye2:
    def __init__(self, url):
        driver.get(url)

        self.handle = driver.current_window_handle

        # 等待登录界面
        waitFor((By.CSS_SELECTOR, ".el-button > span:nth-child(1) > span:nth-child(1)"))

        # login
        eName = driver.find_element_by_css_selector("div.el-form-item:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)")
        eName.clear()
        eName.send_keys('view')
        ePass = driver.find_element_by_css_selector("div.el-form-item:nth-child(3) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)")
        ePass.clear()
        ePass.send_keys('view123')

        driver.find_element_by_css_selector(".el-button > span:nth-child(1) > span:nth-child(1)").click()

        # 进入

        # 等轮播按钮
        waitFor((By.CSS_SELECTOR, ".el-icon-aim"))

        # 点击单屏
        driver.find_element_by_xpath('/html/body/div[2]/div/div/section/div/section/section/header/div[1]/button[1]').click()
        time.sleep(0.2)
        # 点击轮播按钮
        driver.find_element_by_css_selector('.el-icon-aim').click()
        time.sleep(0.2)

        # 等待轮播dlg
        waitFor((By.CSS_SELECTOR, "button.el-button--medium:nth-child(2)"))
        # 选择第一个
        driver.find_element_by_css_selector("td.el-table_1_column_1 > div:nth-child(1) > label:nth-child(1) > span:nth-child(1)").click()
        time.sleep(0.2)
        # 确认
        driver.find_element_by_css_selector('button.el-button--medium:nth-child(2)').click()

        time.sleep(0.5)

        # 点击全屏
        driver.find_element_by_css_selector('.el-icon-rank').click()


    def view(self, span):
        driver.switch_to.window(self.handle)

        time.sleep(span)

    def showTime(self):
        return 30


class ReportEye:
    def __init__(self, url):
        driver.get(url)

        self.handle = driver.current_window_handle

    def view(self, span):
        driver.switch_to.window(self.handle)

        past = 0
        snap = 5
        while past < span:
            maxY = driver.execute_script("return window.scrollMaxY")

            for i in range(0, maxY, 100) :
                driver.execute_script("window.scrollTo(0, %d)" % i)
                time.sleep(snap)
                past += snap
                if past > span:
                    break

    def showTime(self):
        return 60 * 3

def main():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])    
    
    driver = webdriver.Chrome(executable_path="d:/tools/chromedriver.exe", options=options)
    #driver = webdriver.Firefox(firefox_binary='/usr/lib/firefox/firefox')
    driver.fullscreen_window()

    eyes = []
    eyes.append(VideoEye2('https://10.0.224.249/index.html#'))
    

    #~ driver.execute_script("window.open('');")
    #~ driver.switch_to.window(driver.window_handles[1])
    #~ eyes.append(ReportEye('http://10.0.108.222/report/tech.html'))

    #~ driver.switch_to.window(driver.window_handles[0])

    #~ while True:
        #~ for e in eyes:
            #~ e.view(3)

        #~ if time.localtime().tm_hour >= 18:
            #~ break


if __name__ == '__main__':
    main()