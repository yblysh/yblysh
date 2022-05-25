# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:58:45 2022

@author: WIN10
"""

from tkinter import ttk,Label,Tk,Button,Entry
import os
import pandas as pd
import ccxt
import keyboard
import _thread

#分流
def trade(exchange,symbol,side,quantity,price):
    pause()
    df=pd.read_csv('keyandsecret.csv',encoding='ansi',index_col=0)
    while(1):
        print('\n##########################\n')
        print('发送请求中: '+exchange+' '+symbol+' '+side+' '+str(quantity))
        print('\n##########################\n')
        if exchange=='binance':
            key=df['值']['binance的key']
            secret=df['值']['binance的secret']
            client=ccxt.binance({'apiKey':key,'secret':secret}) 
            
        elif exchange=='huobi':
            key=df['值']['huobi的key']
            secret=df['值']['huobi的secret']
            client=ccxt.huobi({'apiKey':key,'secret':secret})
        
        elif exchange=='okx':
            key=df['值']['okx的key']
            secret=df['值']['okx的secret']
            password=df['值']['okx的password']
            client=ccxt.okx({'apiKey':key,'secret':secret,'password':password})
            
        elif exchange=='mexc':
            key=df['值']['mexc的key']
            secret=df['值']['mexc的secret']
            client=ccxt.mexc3({'apiKey':key,'secret':secret})
            
        elif exchange=='gate':
            key=df['值']['gate的key']
            secret=df['值']['gate的secret']
            client=ccxt.gateio({'apiKey':key,'secret':secret})
            
        elif exchange=='ftx':
            key=df['值']['ftx的key']
            secret=df['值']['ftx的secret']
            client=ccxt.ftx({'apiKey':key,'secret':secret})
    
        elif exchange=='bitget':
            key=df['值']['bitget的key']
            secret=df['值']['bitget的secret']
            password=df['值']['bitget的password']
            client=ccxt.bitget({'apiKey':key,'secret':secret,
                                'password':password})
        
        elif exchange=='bybit':
            key=df['值']['bybit的key']
            secret=df['值']['bybit的secret']
            client=ccxt.bybit({'apiKey':key,'secret':secret})
        pause()
        #首先获取价格
        price_now=float(client.fetch_ticker(symbol)['close'])
        print('当前价格')
        print(price_now)
        #if price_now>=price[0] and price_now<=price[1]:
            #下单
        #gateio没有market
        pause()
        if exchange=='gate':
            if side=='SELL':
                p=price[0]
            elif side=='BUY':
                p=price[1]
            client.create_order(symbol,'limit',side,
                                  str(quantity),price=str(p))
        elif exchange=='mexc' and side=='BUY':
            client.create_order(symbol,'market',side,str(quantity),
                                price=price[0])
        else:
            #其他情况用market模式
            client.create_order(symbol,'market',side.lower(),str(quantity))
        pause()
        

#暂停
def pause():
    if keyboard.is_pressed('p'):
        try:
            print('暂停发送请求，关闭程序即可停止，按c键继续')
        except:
            pass
        #按q再开始
        keyboard.wait('c')


#主程序分流
def mainset(prox,exchange,symbol,side,quantity,price):
    os.environ["http_proxy"] = prox
    os.environ["https_proxy"] = prox
    _thread.start_new_thread(trade,(exchange,symbol,side,quantity,price))



#主程序
def main():
    
    #主程序部分
    top = Tk()

    #文字
    Label(top,text='HTTP代理地址为xiyouVPN界面的右上角\n'+
                  '鼠标移动到信号标志上面后可以看到')\
        .grid(row=1, column=5)
        
    Label(top,text='此处输入要买卖的交易符号\n'+
                  '具体交易符号要遵循相应交易所的习惯\n'+\
                  '如binance,huobi,mexc为BTCUSDT\n'+\
                  'okx为BTC-USDT,gate为BTC_USDT\n'+\
                  'ftx为BTC/USD,bitget为BTCUSDT_UMCBL\n'+\
                  'bybit为BTCUSD').grid(row=2, column=5)    
        
    Label(top,text='点击后开始持续发送请求\n'+
                  '如果出错会停下来，请注意返回的信息').grid(row=3, column=5)
    Label(top,text='按p键暂停\n'+
                  '暂停后再按c键继续').grid(row=6, column=5)
    Label(top,text='当币价在这个价格区间时，才会进行交易\n'+
                  '程序会自动采集当前币价'+\
                  '不在区间内不发送请求\n').grid(row=7, column=5)
    Label(top,text='请注意gate没有market模式\n'+
                  '即使用gate交易所时，大于最低价即卖出\n'+\
                  '小于最高价就买入').grid(row=8, column=5)
    
    #输入框
    Label(top,text="HTTP代理地址").grid(row=1, column=0)
    E1=Entry(top,bd=1)
    E1.grid(row=1,column=3)
    E1.insert(0,"http://127.0.0.1:9999")
    Label(top,text="交易所").grid(row=2, column=0)
    E2=ttk.Combobox(top)
    E2.grid(row=2,column=3)
    E2['value']=('binance','huobi','okx','mexc','gate','ftx','bitget','bybit')
    Label(top,text="交易符号").grid(row=3, column=0)
    E3=Entry(top,bd=1)
    E3.grid(row=3,column=3)
    E3.insert(0,"BTCUSDT")

    Label(top,text="数量").grid(row=6, column=0)
    E5=Entry(top,bd=1)
    E5.grid(row=6,column=3)
    E5.insert(0,"1")
    Label(top,text="价格区间最低价格").grid(row=7, column=0)
    E6=Entry(top,bd=1)
    E6.grid(row=7,column=3)
    E6.insert(0,"0")
    Label(top,text="价格区间最高价格").grid(row=8, column=0)
    E7=Entry(top,bd=1)
    E7.grid(row=8,column=3)
    E7.insert(0,"1")


    #按钮    
    Button(top, text ="持续发送买入请求",command=lambda:mainset\
                   (E1.get(),E2.get(),E3.get(),'BUY',E5.get(),
                    (float(E6.get()),float(E7.get()))
                    )
                   ).grid(row=3, column=4)
    Button(top, text ="持续发送卖出请求",command=lambda:mainset\
                   (E1.get(),E2.get(),E3.get(),'SELL',E5.get(),
                    (float(E6.get()),float(E7.get()))
                    )
                   ).grid(row=6, column=4)
    
    
    top.mainloop()

main()

#设置代理
#os.environ["http_proxy"] = "http://127.0.0.1:9999"
#os.environ["https_proxy"] = "http://127.0.0.1:9999"


#trade("http://127.0.0.1:9999",'binance','BTCUSDT','SELL',1,(1,2))
#trade("http://127.0.0.1:9999",'huobi','btcusdt','SELL',1,(1,2)) 
#trade("http://127.0.0.1:9999",'okx','BTC-USDT','SELL',1,(1,2))
#trade("http://127.0.0.1:9999",'mexc','BTCUSDT','SELL',1,(1,2))  
#trade("http://127.0.0.1:9999",'gate','BTC_USDT','SELL',1,(1,2))
#trade("http://127.0.0.1:9999",'ftx','BTC/USD','SELL',1,(1,2))
#trade("http://127.0.0.1:9999",'bitget','BTCUSDT_UMCBL','SELL',1,(1,2)) 
#trade("http://127.0.0.1:9999",'bybit','BTCUSD','SELL',1,(1,2))