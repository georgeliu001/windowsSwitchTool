#!/usr/bin/python3
# coding: utf8

import time

import subprocess
import win32gui, win32con

from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


WM_PLAY = win32con.WM_USER + 100
WM_STOP= win32con.WM_USER + 101

driver = None

def waitFor(locator):
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(locator)
    )


class VideoEye:
    def __init__(self):
        self.startProc()
            
    def startProc(self):
        self.proc = subprocess.Popen([r'C:\Users\Admin\AppData\Local\Programs\Python\Python38\python.exe', r'D:\tools\vplayer\videoplayer.py'], cwd= r'D:\tools\vplayer')
        
        self.hwnd = None
        for i in range(5):
            time.sleep(1)
            hwnd = win32gui.FindWindow('VideoEyeWndClass', None)
            if hwnd:
                self.hwnd = hwnd
                break
                
        if not self.hwnd:
            print("can't find Video wnd")
            return False
            
        return True

    def view(self, span):
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWMAXIMIZED)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
        
        win32gui.PostMessage(self.hwnd, WM_PLAY, 0, 0)
        
        for i in range(span):
            time.sleep(1)
            if not self.proc.poll() is None:
                self.startProc()
                win32gui.PostMessage(self.hwnd, WM_PLAY, 0, 0)
                
        win32gui.PostMessage(self.hwnd, WM_STOP, 0, 0)
        
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWMINNOACTIVE)
        

    def showTime(self):
        return 30
        
    def close(self):
        if self.hwnd:
            win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)


class ReportEye:
    s_urls = []
    def __init__(self, url, showtime=3*60):
        self.showtime = showtime
        
        if len(ReportEye.s_urls) > 0:
            driver.execute_script("window.open('%s');" % url)
        else:
            driver.get(url)
        ReportEye.s_urls.append(url)
        
        self.handle = driver.window_handles[-1]

        self.hwnd = None
        for i in range(10):
            self.hwnd = win32gui.FindWindow('MozillaWindowClass', None)
            if self.hwnd:
                break
            time.sleep(1)
            
    def view(self, span):
        #driver.maximize_window()
        driver.switch_to.window(self.handle)
        if not self.hwnd:
            return
        
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)

        past = 0
        snap = 5
        while past < span:
            maxY = driver.execute_script("return window.scrollMaxY")

            for i in range(0, maxY + 100, 100) :
                driver.execute_script("window.scrollTo(0, %d)" % i)
                time.sleep(snap)
                past += snap
                if past > span:
                    break

    def showTime(self):
        return self.showtime 
        
    def close(self):
        pass

def main():
    global driver
    driver = webdriver.Firefox(executable_path="d:/tools/geckodriver.exe")

    eyes = []
    #eyes.append(VideoEye())

    #~ driver.execute_script("window.open('');")
    #~ driver.switch_to.window(driver.window_handles[1])

    eyes.append(ReportEye('http://10.0.108.222/report/tech.html'))
    eyes.append(ReportEye('http://10.0.108.222/report/prj_plan.png', 60))

    driver.fullscreen_window()

    while True:
        for e in eyes:
            e.view(e.showTime())

        if time.localtime().tm_hour >= 18:
            for e in eyes:
                e.close()
            break

if __name__ == '__main__':
    main()