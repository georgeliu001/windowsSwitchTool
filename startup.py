#coding: utf8

import os, sys
import datetime, json, subprocess
import requests
import bigeye

def isWorkday(day):
    r = requests.get('https://api.apihubs.cn/holiday/get?field=workday&date=%s' % day)
    #print(r.text)
    res = json.loads(r.text)
    return res['data']['list'][0]['workday'] != 2
    
def isTodayWorkday():
    return isWorkday(datetime.date.today().strftime('%Y%m%d'))

if __name__ == '__main__':
    #~ if not isTodayWorkday():
        #~ os.system('shutdown -s')
        #~ sys.exit()
    
    # 启动浏览器
    #subprocess.Popen(["C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", '--kiosk', "http://ax.koal.com/report.html"])
    
    bigeye.main()
