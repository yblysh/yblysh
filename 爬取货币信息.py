# -*- coding: utf-8 -*-
"""
2022年4月22日
"""

from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#import tkinter
import os
import csv
import time
import pandas as pd
import datetime
from pyecharts import options as opts 
from pyecharts.charts import Bar,Page,Line,Pie
import pyecharts
import tkinter


#glassnode调用api
API_KEY='28ji5DRQvAkP9o9A8hEz9LuGujW'
#启动模式
SILENCE = True
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
    # 静默启动 参数组策略
    if SILENCE is True:
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
    options.add_argument('--no-sandbox ')
    options.add_argument('--disable-javascript')
    ##禁止图片加载
    options.add_argument('--blink-settings=imagesEnabled=false')
    #加载ronin wallet
    try:
        options.add_extension("1.7.0_0.crx")
    except:
        print('请将ronin wallet的crx与本程序放到一个文件夹中')
    
    return Chrome(options=options,executable_path=chromedriver_path)

#输出
def output(dic,name):
    #增加TVL变动量
    #上一条记录
    def change(key,dic,last):
        dic[key+'变动']=(dic[key]/last[key].iloc[-1]-1)*100
        dic[key+'变动']=str(round(dic[key+'变动'],4))+'%'
        return dic
    try:
        last=pd.read_csv(str(name),encoding='ANSI')
        dic=change('BTC/ETH的TVL',dic,last)
        dic=change('BTC/USDT的TVL',dic,last)
        dic=change('ETH/USDT的TVL',dic,last)
        dic=change('CAKE/USDT的TVL',dic,last)
        dic=change('SLP/WETH的TVL',dic,last)
        dic=change('DOGE/USDT的TVL',dic,last)
    except:pass
    
    #标题列表
    namelist=['Time','BTC交易所总存量','BTC交易所净流入流出量','BTC(MVRV)','持币数量大于100的地址数量','持币数量大于1000的地址数量','ETH交易所总存量','ETH交易所净流入流出量','STBL交易所中所有稳定币数量','USDT交易所总存量','USDT交易所净流入流出量','USDC交易所总存量','USDC交易所净流入流出量','BTC12小时多单比','BTC12小时空单比','BTC24小时多单比','BTC24小时空单比','BTC获利比','BTC亏损比','USDT当日价格','恐惧贪婪指数','美国10年期国债收益率','纳斯达克收盘价','BTC/ETH的TVL','BTC/ETH的TVL变动','BTC/ETH的收益率','BTC/USDT的TVL','BTC/USDT的TVL变动','BTC/USDT的收益率','BTC价格','BTC相对币量','ETH/USDT的TVL','ETH/USDT的TVL变动','ETH/USDT的收益率','ETH价格','ETH相对币量','CAKE/USDT的TVL','CAKE/USDT的TVL变动','CAKE/USDT的收益率','CAKE价格','CAKE相对币量','SLP/WETH的TVL','SLP/WETH的TVL变动','SLP/WETH的收益率','SLP价格','SLP相对币量','DOGE/USDT的TVL','DOGE/USDT的TVL变动','DOGE/USDT的收益率','DOGE价格','DOGE相对币量','FIL的流通量','FIL的流通率','FIL的质押总量','FIL的销毁量','FIL的全网有效算力','FIL的24小时产出量','FIL的24小时单T平均收益','FIL的新增算力成本','FIL的单T质押量','FIL的单T封装手续费','Binance BTC1日费率','Binance ETH1日费率','Binance BTC7日费率','Binance ETH7日费率','Okex BTC1日费率','Okex ETH1日费率','Okex BTC7日费率','Okex ETH7日费率','Bybit BTC1日费率','Bybit ETH1日费率','Bybit BTC7日费率','Bybit ETH7日费率','FTX BTC1日费率','FTX ETH1日费率','FTX BTC7日费率','FTX ETH7日费率','dYdX BTC1日费率','dYdX ETH1日费率','dYdX BTC7日费率','dYdX ETH7日费率','Gate BTC1日费率','Gate ETH1日费率','Gate BTC7日费率','Gate ETH7日费率','Bitget BTC1日费率','Bitget ETH1日费率','Bitget BTC7日费率','Bitget ETH7日费率','Bitmex BTC1日费率','Bitmex ETH1日费率','Bitmex BTC7日费率','Bitmex ETH7日费率','Huobi BTC1日费率','Huobi ETH1日费率','Huobi BTC7日费率','Huobi ETH7日费率','Deribit BTC1日费率','Deribit ETH1日费率','Deribit BTC7日费率','Deribit ETH7日费率']
    
    #输出列表
    outlist=[]
    for i in namelist:
        try:
            outlist.append(dic[i])
        except:
            outlist.append('')
    try:
        if not os.path.exists(str(name)):
            file=open(str(name),'w',newline='',errors='ignore')
            csv_writer = csv.writer(file)
            csv_writer.writerow(namelist)
        else:
            file=open(str(name),'a',newline='',errors='ignore')
            csv_writer = csv.writer(file)
    except:
        if not os.path.exists(str(name)):
            print('输出文件无法建立')
        else:
            print('输出文件无法打开，请不要在程序运行时打开输出文件')
    try:
        csv_writer.writerow(outlist)
    except:
        print('无法输出数据')
    file.close()


def creep(name):
    
    #设定driver
    #capa = DesiredCapabilities.CHROME
    #capa["pageLoadStrategy"] = "NORMAL"
    driver=set_spider_option("chromedriver.exe")
    #设置总字典
    dic={}
    
    #BTC12小时多空比
    url='https://www.coinglass.com/zh/LongShortRatio'
    driver.get(url)
    
    #检查有没有变成12小时的指示变量
    temp=-1
    while temp==-1:

        #点击12小时
        try:
            #点击区间下拉菜单
            driver.find_elements_by_class_name(
                                 'ant-select-selection-item')[1].click()
            time.sleep(0.5)
            driver.find_elements_by_class_name(
                             'ant-select-item-option-content')[5].click()
        except:pass
        #检查有没有变成12小时
        time.sleep(0.5)
        temp=driver.find_elements_by_class_name(
                        'ant-select-selection-item')[1].text.find('12')
        
    
    #从camera按钮缓慢移动到表格
    target=driver.find_element_by_class_name('anticon-camera')
    for i in range(20,500,4):
        ActionChains(driver)\
        .move_to_element_with_offset(target,-i,50).perform()
        #检查有没有碰到表格
        table=driver.find_element_by_class_name('bybt-chart-tooltip')
        if table.get_attribute('style').find('hidden')==-1 and\
            table.get_attribute('style')!='':
            dic['BTC12小时多单比']=table.find_element_by_xpath(
                                    '//strong[1]').text.replace('%','')
            dic['BTC12小时空单比']=table.find_element_by_xpath(
                                    '//strong[2]').text.replace('%','')
            break
    
    #BTC24小时多空比
    
    #检查有没有变成24小时的指示变量
    temp=-1
    while temp==-1:
        
        #点击24小时
        try:
            #点击区间下拉菜单
            driver.find_elements_by_class_name(
                                 'ant-select-selection-item')[1].click()
            time.sleep(0.5)
            driver.find_elements_by_class_name(
                             'ant-select-item-option-content')[6].click()
        except:pass
        time.sleep(0.5)
        #检查有没有变成24小时
        temp=driver.find_elements_by_class_name(
                        'ant-select-selection-item')[1].text.find('24')
    
    #从camera按钮缓慢移动到表格
    target=driver.find_element_by_class_name('anticon-camera')
    for i in range(20,500,4):
        ActionChains(driver)\
        .move_to_element_with_offset(target,-i,50).perform()
        #检查有没有碰到表格
        table=driver.find_element_by_class_name('bybt-chart-tooltip')
        if table.get_attribute('style').find('hidden')==-1 and\
            table.get_attribute('style')!='':
            #BTC24小时多空比
            dic['BTC24小时多单比']=table.find_element_by_xpath(
                                    '//strong[1]').text.replace('%','')
            dic['BTC24小时空单比']=table.find_element_by_xpath(
                                    '//strong[2]').text.replace('%','')
            break
    
    #BTC获利亏损比
    url='https://app.intotheblock.com/coin/BTC'
    driver.get(url)
    temp=-1
    while temp==-1:
        try:
            dic['BTC获利比']=driver.find_elements_by_class_name(
                                       'value')[0].text.replace('%','')
            dic['BTC亏损比']=driver.find_elements_by_class_name(
                                       'value')[2].text.replace('%','')
            temp=dic['BTC获利比']
        except:time.sleep(0.1)
    
    #USDT当日价格
    url='https://coinyep.com/zh/ex/USDT-CNY'
    driver.get(url)
    temp=''
    while temp=='':
        try:
            coinyep=driver.find_element_by_id('coinyep-reverse1').text
            temp=coinyep
        except:time.sleep(0.1)
    dic['USDT当日价格']=float(coinyep[coinyep.find('=')+1:coinyep.find('CNY')])
    
    #恐惧贪婪指数
    url='https://www.coinglass.com/zh'
    driver.get(url)
    dic['恐惧贪婪指数']=''
    while dic['恐惧贪婪指数']=='':
        time.sleep(0.1)
        dic['恐惧贪婪指数']=driver.find_element_by_xpath(
            "//div[@class='bybt-home-minicharbox']//div[2]").text
    
    
    #美国10年期国债收益率
    url='https://wallstreetcn.com/markets/codes/US10YR.OTC'
    driver.get(url)
    temp=''
    while temp=='':
        try:
            dic['美国10年期国债收益率']=driver.find_element_by_class_name(
                                                    'price-lastpx').text
            temp=dic['美国10年期国债收益率']
        except:time.sleep(0.1)
        
    #纳斯达克收盘价
    url='http://quote.eastmoney.com/gb/zsNDX.html'
    driver.get(url)
    temp=''
    while temp=='':
        try:
            dic['纳斯达克收盘价']=driver.find_element_by_class_name(
                                                'zxj').text
            temp=dic['纳斯达克收盘价']
        except:time.sleep(0.1)
    

    #全网BTC合约实盘持仓量
    url='https://www.coinglass.com/zh/BitcoinOpenInterest'
    driver.get(url)
    temp=0
    while temp<12:
        try:
            #首先定位表格
            table=driver.find_element_by_class_name('bybt-box')
            #然后定位行
            row=table.find_elements_by_class_name('ant-row')
            temp=len(row)
        except:time.sleep(0.1)
    #爬取并写入dataframe
    df=[]
    #取前十交易所,合计占一行，表头占一行
    for i in range(12):
        df.append(row[i].text.split('\n'))
    #补齐合计那一行的数据
    if len(df[0])==8:
        df[1]=['#']+df[1]
    positionTable=pd.DataFrame(df[1:],columns=df[0])
    
    #记录当前时间
    dic['Time']=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    positionTable.to_csv('持仓量csv\\'+dic['Time']+'.csv',encoding='ansi')
    
    
    #资金费率1日费率
    url='https://www.coinglass.com/zh/FundingRate'
    driver.get(url)
    temp=0
    while temp<10:
        try:
            #爬取交易所名称
            column=[i.text for i in driver.find_elements_by_class_name(
                                                        'display-flex')]
            temp=len(column)
        except:time.sleep(0.1)
    
    #点击1日费率
    driver.find_elements_by_class_name('radio-item')[1].click()
    #爬取btc
    btc_1=[]
    for i in driver.find_elements_by_class_name('shouPredicted'):
        temp=i.text.split('\n')[0]
        if temp!='BTC' and temp!='':
            btc_1.append(temp)
            
    #定位左表和右表
    left=driver.find_elements_by_class_name('fr-box')[1]
    right=driver.find_elements_by_class_name('fr-box')[3]
    #爬取eth
    eth_1=[]
    for i in left.find_elements_by_class_name('hidePredicted'):
        eth_1.append(i.text)
        if len(eth_1)>=7:
            break
    for i in right.find_elements_by_class_name('hidePredicted'):
        eth_1.append(i.text)
        if len(eth_1)>=14:
            break
    
    
    #资金费率7日费率
    #点击7日费率
    driver.find_elements_by_class_name('radio-item')[2].click()
    #爬取btc
    btc_7=[]
    for i in driver.find_elements_by_class_name('shouPredicted'):
        temp=i.text.split('\n')[0]
        if temp!='BTC' and temp!='':
            btc_7.append(temp)
            
    #定位左表和右表
    left=driver.find_elements_by_class_name('fr-box')[1]
    right=driver.find_elements_by_class_name('fr-box')[3]
    #爬取eth
    eth_7=[]
    for i in left.find_elements_by_class_name('hidePredicted'):
        eth_7.append(i.text)
        if len(eth_7)>=7:
            break
    for i in right.find_elements_by_class_name('hidePredicted'):
        eth_7.append(i.text)
        if len(eth_7)>=14:
            break
    
    for i in range(len(column)):
        dic[column[i]+'BTC1日费率']=btc_1[i]
        dic[column[i]+'ETH1日费率']=eth_1[i]
        dic[column[i]+'BTC7日费率']=btc_7[i]
        dic[column[i]+'ETH7日费率']=eth_7[i]
    
    
    #FIL的爬取
    url='https://filfox.info/zh'
    driver.get(url)
    #点掉foxwallet叉
    driver.find_element_by_class_name('w-4').click()
    #全部爬取
    filList=driver.find_elements_by_class_name('text-left')
    #点击展开
    try:
        driver.find_element_by_class_name('el-button').click()
    except:
        driver.find_elements_by_class_name('el-button')[1].click()
    
    filDic={}
    for i in range(int(len(filList)/2)):
        filDic[filList[2*i].text]=filList[2*i+1].text
    
    #FIL的流通量
    dic['FIL的流通量']=filDic['FIL流通量'][:-3].replace(',','')
    
    #FIL的流通率
    dic['FIL的流通率']=filDic['FIL流通率'].replace('%','')
    
    #FIL的质押总量
    dic['FIL的质押总量']=filDic['FIL质押量'][:-3].replace(',','')
    
    #FIL的销毁量
    dic['FIL的销毁量']=filDic['FIL销毁量'][:-3].replace(',','')
    
    #FIL的全网有效算力
    dic['FIL的全网有效算力']=filDic['全网有效算力'][:-3]
    
    #FIL的24小时产出量
    dic['FIL的24小时产出量']=filDic['近24h产出量'][:-3].replace(',','')
    
    #FIL的24小时单T平均收益
    dic['FIL的24小时单T平均收益']=filDic['24h平均提供存储服务收益'][:-7]
    
    #FIL的新增算力成本
    dic['FIL的新增算力成本']=float(filDic['新增算力成本'][:-7])
    
    #FIL的单T质押量（记得*32）
    dic['FIL的单T质押量']=float(filDic['当前扇区质押量'][:-9])*32
    
    #FIL的单T封装手续费（新增算力成本-FIL的单T质押量）
    dic['FIL的单T封装手续费']=dic['FIL的新增算力成本']-dic['FIL的单T质押量']
    
    
    
    #BTC/ETH的TVL（m换成百万）（两个网站加总）
    url='https://info.uniswap.org/#/pools/0xcbcdf9626bc03e24f779434178a73a0b4bad62ed'
    driver.get(url)
    #等待加载
    temp=-1
    while temp==-1:
        try:
            temp=driver.find_element_by_class_name(
                                     'css-5omc5c').text.find('$')
        except:pass
        time.sleep(0.1)
    
    dic['BTC/ETH的TVL']=int(float(driver.find_element_by_class_name(
                 'css-5omc5c').text.replace('$','').replace('m',''))*1e6)
    
    
    #BTC/USDT的TVL（m换成百万）（两个网站加总）
    url='https://info.uniswap.org/#/pools/0x99ac8ca7087fa4a2a1fb6357269965a2014abc35'
    driver.get(url)
    #等待加载
    temp=-1
    while temp==-1:
        try:
            temp=driver.find_element_by_class_name(
                                     'css-5omc5c').text.find('$')
        except:pass
        time.sleep(0.1)
    dic['BTC/USDT的TVL']=int(float(driver.find_element_by_class_name(
                 'css-5omc5c').text.replace('$','').replace('m',''))*1e6)
    
    
    
    #ETH/USDT的TVL（m换成百万）（两个网站加总）
    url='https://info.uniswap.org/#/pools/0x4e68ccd3e89f51c3074ca5072bbac773960dfa36'
    driver.get(url)
    #等待加载
    temp=-1
    while temp==-1:
        try:
            temp=driver.find_element_by_class_name(
                                     'css-5omc5c').text.find('$')
        except:pass
        time.sleep(0.1)
    
    dic['ETH/USDT的TVL']=int(float(driver.find_element_by_class_name(
                 'css-5omc5c').text.replace('$','').replace('m',''))*1e6)
    
    
    #前往另一个网站
    url='https://pancakeswap.finance/farms'
    driver.get(url)
    
    #pancakeswap.finance/farms 构造函数
    def get_pancake(key):
        #搜索key
        #清空搜索框并输入key
        driver.find_element_by_class_name('hUTEqD').clear()
        driver.find_element_by_class_name('hUTEqD').clear()
        time.sleep(0.5)
        driver.find_element_by_class_name(
                            'hUTEqD').send_keys(key)
        #等待搜索结果出现
        temp=-1
        while temp==-1:
            temp=driver.find_elements_by_class_name(
                                'eOXvol')[-1].text.find(key)
            time.sleep(0.5)
        #得到TVL和APR
        temp=0
        while temp==0:
            try:
                TVL=int(driver.find_elements_by_class_name(
                     'iwlkGu')[-1].text.replace(',','').replace('$',''))
                APR=float(driver.find_element_by_class_name(
                     'gyWaRu').text.split('\n')[0].replace('%',''))
                temp=TVL
            except:time.sleep(0.1)
        return TVL,APR
    
    #搜索BTCB-ETH
    temp=get_pancake('BTCB-ETH')
    #BTC/ETH的TVL
    dic['BTC/ETH的TVL']+=temp[0]
    #BTC/ETH的收益率
    dic['BTC/ETH的收益率']=temp[1]/2
    
    #搜索BTCB-BUSD
    temp=get_pancake('BTCB-BUSD')
    #BTC/USDT的TVL
    dic['BTC/USDT的TVL']+=temp[0]
    #BTC/USDT的收益率另一个
    dic['BTC/USDT的收益率']=temp[1]
    
    #搜索ETH-USDC
    temp=get_pancake('ETH-USDC')
    #ETH/USDT的TVL
    dic['ETH/USDT的TVL']+=temp[0]
    #ETH/USDT的收益率另一个
    dic['ETH/USDT的收益率']=temp[1]
    
    #搜索CAKE-USDT
    temp=get_pancake('CAKE-USDT')
    #CAKE/USDT的TVL（两个usd相加）
    dic['CAKE/USDT的TVL']=temp[0]    
    #CAKE/USDT的收益率
    dic['CAKE/USDT的收益率']=temp[1]/2
    
    #搜索CAKE-BUSD
    temp=get_pancake('CAKE-BUSD')
    #CAKE/USDT的TVL（两个usd相加）
    dic['CAKE/USDT的TVL']+=temp[0]
    #CAKE/USDT的收益率另一个
    dic['CAKE/USDT的收益率']+=temp[1]/2
    
    
    #SLP/WETH的TVL（钱包问题）扩展程序就是为了获得此数据
    url='https://katana.roninchain.com/#/farm'
    driver.get(url)
    
    #这个需要页面加载完毕，即没有--了
    i=0
    temp=0
    while temp!=-1:
        try:
            temp=driver.find_elements_by_class_name(
                                  'leading-20')[9].text.find('-')
        except:
            pass
        time.sleep(0.1)
        i+=1
        if i>100:
            driver.get(url)
    
    #SLP/WETH的TVL
    dic['SLP/WETH的TVL']=int(driver.find_elements_by_class_name(
                'leading-20')[7].text.replace(',','').replace('$',''))
    
    #SLP/WETH的收益率
    dic['SLP/WETH的收益率']=driver.find_elements_by_class_name(
                                'leading-20')[9].text.replace('%','')
    
    
    #DOGE/USDT的TVL（搜索doge）
    url='https://apy.top/home'
    driver.get(url)
    #等待加载
    temp=0
    while temp==0:
        try:
            #点击输入栏
            driver.find_element_by_class_name('el-input').click()
            temp=driver.find_element_by_class_name('el-input').text
        except:time.sleep(0.1)
    #输入DOGE
    driver.find_element_by_class_name(
                        'el-input__inner').send_keys('DOGE')
    temp=-1
    while temp==-1:
        try:
            temp=driver.find_element_by_class_name('link').\
                find_elements_by_class_name('item')[1].text.find('DOGE')
        except:time.sleep(0.1)

    #点击DOGE
    driver.execute_script('document.getElementsByClassName("type")[1].click()')
    time.sleep(1)
    #筛选得到的结果
    temp=-1
    while temp==-1:
        try:
            #等待结果出来
            for i in driver.find_elements_by_class_name('el-table__row'):
                #找到了狗狗币
                if i.find_element_by_class_name('fiex-token').text=='DOGE-USDT':
                    dic['DOGE/USDT的TVL']=int(float(i.find_elements_by_class_name(
                                    'platformName')[1].text.replace('M',''))*1e6)
            #DOGE/USDT的收益率
                    dic['DOGE/USDT的收益率']=float(i.find_element_by_class_name(
                                    'value').text.replace('%',''))
                    temp=dic['DOGE/USDT的TVL']
                    break
        except:time.sleep(0.1)

        
        
    #币价和相对币量
    #相对币量=tvl/币价
    url='https://www.binance.com/zh-CN/markets'
    driver.get(url)
    temp=-1
    while temp==-1:
        try:
            temp=driver.find_element_by_class_name('css-ovtrou').text
        except:time.sleep(0.1)

    row=driver.find_elements_by_class_name('css-vlibs4')
    for i in row:
        if i.text.find('BTC\nBitcoin')!=-1:
            #BTC币价和相对币量
            dic['BTC价格']=float(i.find_element_by_class_name(
                        'css-ovtrou').text.replace(',','').replace('$',''))
            dic['BTC相对币量']=dic['BTC/USDT的TVL']/dic['BTC价格']
        elif i.text.find('ETH\nEthereum')!=-1:
            #ETH币价和相对币量
            dic['ETH价格']=float(i.find_element_by_class_name(
                        'css-ovtrou').text.replace(',','').replace('$',''))
            dic['ETH相对币量']=dic['ETH/USDT的TVL']/dic['ETH价格']
        elif i.text.find('DOGE\n')!=-1:
            #DOGE币价和相对币量
            dic['DOGE价格']=float(i.find_element_by_class_name(
                        'css-ovtrou').text.replace(',','').replace('$',''))
            dic['DOGE相对币量']=dic['DOGE/USDT的TVL']/dic['DOGE价格']
        elif i.text.find('CAKE\n')!=-1:
            #ETH币价和相对币量
            dic['CAKE价格']=float(i.find_element_by_class_name(
                        'css-ovtrou').text.replace(',','').replace('$',''))
            dic['CAKE相对币量']=dic['CAKE/USDT的TVL']/dic['CAKE价格']
    
    #SLP要查找才能找到
    driver.find_element_by_id('markets_main_search').send_keys('smoot')
    time.sleep(0.5)
    #分段反应
    driver.find_element_by_id('markets_main_search').send_keys('h')
    dic['SLP价格']=float(driver.find_element_by_class_name(
                'css-ovtrou').text.replace(',','').replace('$',''))
    dic['SLP相对币量']=dic['SLP/WETH的TVL']/dic['SLP价格']
    
    
    #BTC交易所总存量
    #1650240000是时间戳，减少加载时间
    url='https://api.glassnode.com/' +\
        'v1/metrics/distribution/balance_exchanges?'+\
        'a=BTC&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['BTC交易所总存量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #BTC交易所净流入流出量
    url='https://api.glassnode.com/' +\
        'v1/metrics/transactions/transfers_volume_exchanges_net?'+\
        'a=BTC&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['BTC交易所净流入流出量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #BTC(MVRV)
    url='https://api.glassnode.com/' +\
        'v1/metrics/market/mvrv?'+\
        'a=BTC&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['BTC(MVRV)']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #持币数量大于100的地址数量
    url='https://api.glassnode.com/' +\
        'v1/metrics/addresses/min_100_count?'+\
        'a=BTC&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['持币数量大于100的地址数量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    #持币数量大于1000的地址数量
    url='https://api.glassnode.com/' +\
        'v1/metrics/addresses/min_1k_count?'+\
        'a=BTC&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['持币数量大于1000的地址数量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #ETH交易所总存量
    url='https://api.glassnode.com/' +\
        'v1/metrics/distribution/balance_exchanges?'+\
        'a=ETH&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['ETH交易所总存量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #ETH交易所净流入流出量
    url='https://api.glassnode.com/' +\
        'v1/metrics/transactions/transfers_volume_exchanges_net?'+\
        'a=ETH&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['ETH交易所净流入流出量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    
    #STBL交易所中所有稳定币数量
    url='https://api.glassnode.com/' +\
        'v1/metrics/distribution/balance_exchanges?'+\
        'a=STBL&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['STBL交易所中所有稳定币数量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]

    #USDT交易所总存量
    url='https://api.glassnode.com/' +\
        'v1/metrics/distribution/balance_exchanges?'+\
        'a=USDT&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['USDT交易所总存量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #USDT交易所净流入流出量
    url='https://api.glassnode.com/' +\
        'v1/metrics/transactions/transfers_volume_exchanges_net?'+\
        'a=USDT&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['USDT交易所净流入流出量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #USDC交易所总存量
    url='https://api.glassnode.com/' +\
        'v1/metrics/distribution/balance_exchanges?'+\
        'a=USDC&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['USDC交易所总存量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    #USDC交易所净流入流出量
    url='https://api.glassnode.com/' +\
        'v1/metrics/transactions/transfers_volume_exchanges_net?'+\
        'a=USDC&s=1650240000&api_key='+API_KEY
    driver.get(url)
    dic['USDC交易所净流入流出量']=pd.read_json(driver.find_element_by_xpath(
                                                './*').text).iloc[-1,-1]
    
    
    #结束，把网站关了
    driver.close()
    
    #记录当前时间
    

    output(dic,name)

def plot_data_():
    
    
    #读取数据
    df=pd.read_csv('out.csv',encoding='ANSI')
    
    #对数据分类：
    #比率类
    percent=['BTC12小时多单比','BTC12小时空单比','BTC24小时多单比',
             'BTC24小时空单比','BTC获利比','BTC亏损比']
    percent_p=Line(init_opts=opts.InitOpts(chart_id=1))
    percent_p.add_xaxis(list(df['Time']))
    for i in percent:
        percent_p.add_yaxis(i,list(df[i]))
    percent_p.set_global_opts(title_opts=opts.TitleOpts(title=""),
                              datazoom_opts=[opts.DataZoomOpts()])

    
    a=(Line(init_opts=opts.InitOpts(chart_id=2))
    .add_xaxis(list(df['Time']))
    .add_yaxis('BTC交易所总存量',list(df['BTC交易所总存量']),)
    .set_global_opts(title_opts=opts.TitleOpts(title=""),
                            datazoom_opts=[opts.DataZoomOpts()])
    )
    b=(Line(init_opts=opts.InitOpts(chart_id=3))
    .add_xaxis(list(df['Time']))
    .add_yaxis('ETH交易所总存量',list(df['ETH交易所总存量']))
    .set_global_opts(title_opts=opts.TitleOpts(title=""),
                            datazoom_opts=[opts.DataZoomOpts()])
    )
    c=(Line(init_opts=opts.InitOpts(chart_id=4))
    .add_xaxis(list(df['Time']))
    .add_yaxis('USDC交易所总存量',list(df['USDC交易所总存量']))
    .set_global_opts(title_opts=opts.TitleOpts(title=""),
                            datazoom_opts=[opts.DataZoomOpts()])
    )
    d=(Line(init_opts=opts.InitOpts(chart_id=5))
    .add_xaxis(list(df['Time']))
    .add_yaxis('USDT交易所总存量',list(df['USDT交易所总存量']))
    .set_global_opts(title_opts=opts.TitleOpts(title=""),
                            datazoom_opts=[opts.DataZoomOpts()])
    )
    
    total=(
        Line(init_opts=opts.InitOpts(chart_id=0))
        .add_xaxis(list(df['Time']))
        .add_yaxis('BTC交易所总存量',list(df['BTC交易所总存量']))
        .add_yaxis('ETH交易所总存量',list(df['ETH交易所总存量']))
        .add_yaxis('USDC交易所总存量',list(df['USDC交易所总存量']))
        .add_yaxis('USDT交易所总存量',list(df['USDT交易所总存量']))
        .set_global_opts(title_opts=opts.TitleOpts(title=""),
                                datazoom_opts=[opts.DataZoomOpts()],
                        yaxis_opts=opts.AxisOpts(),)
        )
    
    e=(Line(init_opts=opts.InitOpts(chart_id=6))
    .add_xaxis(list(df['Time']))
    .set_global_opts(title_opts=opts.TitleOpts(title=""),
                            datazoom_opts=[opts.DataZoomOpts()]))
    for i in ['BTC/ETH的TVL','BTC/USDT的TVL','ETH/USDT的TVL','CAKE/USDT的TVL',
              'SLP/WETH的TVL','DOGE/USDT的TVL']:
        e.add_yaxis(i,list(df[i]))
    
    
    #最新的持仓量柱状图
    for i in os.walk('持仓量csv'):
        fileList=i[2]
        #加个break可以不深入遍历子文件夹
        break
    pos=pd.read_csv('持仓量csv\\'+fileList[-1],index_col=0,encoding='ansi')
    #数据处理
    def wanyijia(x):
        if x.find('万')!=-1:
            return float(x.replace('万',''))*1e4
        elif x.find('亿')!=-1:
            return float(x.replace('亿',''))*1e8
        elif x.find('%')!=-1:
            return float(x.replace('%',''))
        return float(x)

    
    
    
    pos.iloc[:,2:]=pos.iloc[:,2:].apply(\
                            lambda x:x.apply(lambda y:float(wanyijia(y))))
    pos_bar=Bar(init_opts=opts.InitOpts(chart_id=7))
    pos_bar.add_xaxis(list(pos['交易所']))
    for i in ['持仓(BTC)','持仓($)','占比','1小时变化','4小时变化','24小时变化']:
        pos_bar.add_yaxis(i,list(pos[i]))
    pos_bar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-25))
                     ,title_opts=opts.TitleOpts(title=""))
    
    
    
    pie=(Pie(init_opts=opts.InitOpts(chart_id=8))
        .add("", [list(z) for z in zip(pos['交易所'].iloc[1:],
                    pos['持仓(BTC)'].iloc[1:])])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
    )
    page=(
        Page(layout=Page.DraggablePageLayout)
        .add(total,percent_p,e,pos_bar,pie)
    )
    page.render("out.html")
    #page.save_resize_html('out.html',cfg_file='chart_config.json',dest='out_json.html')

def timing_creep():
    had=0
    while(1):
        
        #要做的那个小时有没有已经爬取过了
        #每天四次
        if int(datetime.datetime.now().strftime('%H')) in [0,4,8,12,16,20]:
            #如果没执行
            if had==0:
                try:
                    creep('out.csv')
                    plot_data_()
                    had=1
                except:pass
        else:
            had=0
        #歇60秒检查一次
        for i in range(60):
            time.sleep(1)

        
def main():
    
    top = tkinter.Tk()
    top.title('爬取')

    tkinter.Button(top, text ="爬取",command=lambda:creep('out.csv'))\
        .grid(row=12, column=4)
    tkinter.Button(top, text ="生成表格",command=lambda:\
               plot_data_()).grid(row=13, column=4)
    tkinter.Button(top, text ="定时爬取",command=lambda:\
               timing_creep()).grid(row=14, column=4)
        
    top.mainloop()
    

main()


