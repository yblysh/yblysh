# -*- coding: utf-8 -*-
"""
Created on Thu May  5 11:05:24 2022

@author: WIN10
"""

from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.by import By
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#import os


#chrome初始化
def set_spider_option(chromedriver_path=None) -> Chrome:
    # 调整chromedriver的读取路径，若不指定则尝试从环境变量中查找
    try:
        chromedriver_path = "chromedriver.exe" \
            if chromedriver_path is None else chromedriver_path
    except:
        print('请将chromedriver.exe与本程序放到一个文件夹中')
    # 实例化Chrome可选参数
    options = ChromeOptions()

    # 无头模式
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-software-rasterizer")
    # 其他推荐设置
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    options.add_experimental_option('excludeSwitches',['enable-automation'])
    #全屏启动
    options.add_argument('--start-maximized') 
    options.add_argument('--disable-javascript')
    ##禁止图片加载
    options.add_argument('--blink-settings=imagesEnabled=false')

    return Chrome(options=options,executable_path=chromedriver_path)




#各交易所公告列表
dic={}
#要post的公告和网址列表
post=[]

driver=set_spider_option("chromedriver.exe")
driver.minimize_window()


#获得公告列表
def get_announce(url,announce_name):
    out={}
    try:
        driver.get(url)
    
        #定位所有公告
        announce=[]
        while len(announce)==0:
            announce=driver.find_elements(By.CLASS_NAME,announce_name)
            time.sleep(0.2)
        #公告名称列表和网址列表
        for i in range(len(announce)):
            #如果是gate，那href得往上找
            if announce_name=='to-startup-detail':
                out[announce[i].get_attribute('title')]=announce[i].get_attribute('href')
            else:
                out[announce[i].text]=announce[i].get_attribute('href')
    except:
        pass
    return out


#每个交易所公告和公告元素class
#打表然后统一操作
exchange={
    'binance':['https://www.binance.com/zh-CN/support/announcement/c-48?navId=48','css-1ey6mep'],
    'huobi':['https://www.huobi.com/support/zh-cn/list/360000039942','list-field1'],
    'okx':['https://www.okx.com/support/hc/zh-cn/sections/115000447632-%E6%96%B0%E5%B8%81%E4%B8%8A%E7%BA%BF','article-list-link'],
    'mexc':['https://support.mexc.com/hc/zh-cn/sections/360000547811-%E6%96%B0%E5%B8%81%E4%B8%8A%E6%96%B0','article-list-link'],
    'gate':['https://www.gate.io/cn/startup','to-startup-detail'],
    'ftx':['https://help.ftx.com/hc/zh-cn/sections/360007186612-%E4%B8%8A%E6%96%B0%E5%85%AC%E5%91%8A','sections-list'],
    'bitget':['https://bitget.zendesk.com/hc/zh-cn/sections/5955813039257-%E6%96%B0%E5%B8%81%E4%B8%8A%E7%BA%BF','article-list-link']
    }


for i in exchange:
    #获得当前公告列表
    dic[i]=get_announce(exchange[i][0],exchange[i][1])
    
#huobi推特爬取
def get_twitter():
    url='https://twitter.com/HuobiGlobal'
    driver.get(url)
    out={}
    while len(out.keys())<5:
        announce=[]
        while len(announce)==0:
            announce=driver.find_elements(By.XPATH,"/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/div[@class='css-1dbjc4n'][2]")
            time.sleep(0.1)
        #公告名称列表和网址列表
        for i in announce:
            try:
                string=i.text
                string=string[:string.rfind('\n')]
                string=string[:string.rfind('\n')]
                string=string[:string.rfind('\n')]
                try:
                    out[string]=i.find_element(By.PARTIAL_LINK_TEXT,'http').\
                                                        get_attribute('href')
                except:
                    out[string]=''
            except:pass
        driver.execute_script('window.scrollBy(0,200)')
        time.sleep(0.1)
    return out

dic['huobi_twitter']=get_twitter()


while 1:
    #休息5分钟，防止被发现是爬虫
    for i in range(300):
        time.sleep(1)
    for i in exchange:
        url=exchange[i][0]
        #获得当前公告列表
        temp=get_announce(exchange[i][0],exchange[i][1])
        #计算上一次储存的公告列表与新得到的差,也就是看新列表多了什么
        newAnnounce=list(set(temp)-set(dic[i]))
        #记录新的公告列表
        dic['binance']=temp
        #记录要发送的新公告
        #这里假定交易所不可能一次性发五个新公告，一定是程序出错了
        if len(newAnnounce)<5:
            for j in newAnnounce:
                post.append(i+'的新公告：\n'+j+'\n'+dic[j])
    
    #huobi推特的primelist推送
    temp=get_twitter()
    #计算上一次储存的公告列表与新得到的差,也就是看新列表多了什么
    newAnnounce=list(set(temp)-set(dic['huobi_twitter']))
    #点击
    dic['huobi_twitter']=temp
    #记录要发送的新公告
    for j in newAnnounce:
        #有primelist才发
        if j.lower().find('primelist')!=-1:
            post.append('huobi的新primelist：\n'+j+'\n'+dic[j])
        
        
    #此时已经记录了所有的post，如果有消息就准备发送
    if len(post)>0:
        poststr='\n'.join(post)
        
        
        # 发信方的信息：发信邮箱，QQ 邮箱授权码
        from_addr = 'mangsheyihao1st@163.com'
        password = 'UMDTTQFPWTDTIXOM'
        # 收信方邮箱
        to_addr = 'warrenhuobi@163.com'
        
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(poststr,'plain','utf-8')
        msg['From'] = Header('消息提醒')
        msg['Subject'] = Header('新公告提醒')
        
        # 发信服务器
        smtp_server = 'smtp.163.com'
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server,465)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()


