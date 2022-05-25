# -*- coding: utf-8 -*-
"""
Created on Sun May 15 15:07:37 2022

@author: WIN10
"""

from tkinter import ttk,Label,Tk,Button,Entry
from os import path,environ
from csv import writer
from pandas import DataFrame,read_json
from time import strftime,localtime
from requests import get




#输出
def output(dic,name):
    #标题列表
    namelist=['交易所','币种','开盘价','1分钟涨幅','1分钟回撤','1分钟的交易总额',
              '5分钟涨幅','5分钟回撤','5分钟的交易总额','15分钟涨幅','15分钟回撤',
              '15分钟的交易总额','1小时涨幅','1小时回撤','1小时交易总额','1日涨幅',
              '1日回撤','1日交易总额','1周涨幅','1周回撤','1周交易总额','1月涨幅',
              '1月回撤','1月交易总额','历史最高价','历史最高价时间','历史最低价',
              '历史最低价时间','目前币价']
    #输出列表
    outlist=[]
    for i in namelist:
        try:
            outlist.append(dic[i])
        except:
            outlist.append('')
    try:
        if not path.exists(str(name)):
            file=open(str(name),'w',newline='',errors='ignore')
            csv_writer = writer(file)
            csv_writer.writerow(namelist)
        else:
            file=open(str(name),'a',newline='',errors='ignore')
            csv_writer = writer(file)
    except:
        if not path.exists(str(name)):
            print('输出文件无法建立')
        else:
            print('输出文件无法打开，请不要在程序运行时打开输出文件')
    try:
        csv_writer.writerow(outlist)
    except:
        print('无法输出数据')
    file.close()

def sql_binance(symbol,interval,from_time,limit):
    #只接受大写
    symbol=symbol.upper()
    #接收的参数需要更改时间位数
    from_time=str(int(from_time)*1000)
    #发送请求
    url='https://api.binance.com/api/v3/klines'
    param={
        'symbol':symbol,'interval':interval,
        'startTime':from_time,'limit':limit
        }
    response=get(url=url,params=param)
    out=read_json(response.text)
    #表格命名
    out.columns=['open_time','open','high','low','close','','','volume',
                 '','','','']
    #更改时间位数
    out['open_time']=out['open_time'].apply(lambda x:int(x/1000))
    
    return out

def sql_huobi(symbol,interval,from_time,limit):
    #只接受小写
    symbol=symbol.lower()
    url='https://api.huobi.pro/market/history/kline'
    param={
        'symbol':symbol,'period':interval,'size':1999
        }
    response=get(url=url,params=param)
    try:
        out=DataFrame(list(read_json(response.text)['data']))
    except:
        raise Exception(response.text)
    #表格命名
    out.columns=['open_time','open','close','low','high','amount','volume',
                  'count']
    return out

def sql_okx(symbol,interval,from_time,limit):
    #链接并不稳定，基本没啥用
    #只接受大写
    symbol=symbol.upper()
    url='https://www.okx.com/api/v5/market/history-candles'
    #接收的参数需要更改时间位数
    from_time=int(from_time*1000)
    if limit>=100:
        limit=99
    param={
        'instId':symbol,'bar':interval,'before':from_time,'limit':limit
        }
    response=get(url=url,params=param)
    try:
        out=DataFrame(list(read_json(response.text)['data']))
    except:
        raise Exception(response.text)
    #表格命名
    out.columns=['open_time','open','high','low','close','amount','volume']
    #更改时间位数
    out['open_time']=out['open_time'].apply(lambda x:int(int(x)/1000))
    return out

def sql_mexc(symbol,interval,from_time,limit):
    #只接受大写
    symbol=symbol.upper()
    #接收的参数需要更改时间位数
    from_time=int(from_time*1000)
    #发送请求
    url='https://api.mexc.com/api/v3/klines'
    param={
        'symbol':symbol,'interval':interval,
        'startTime':from_time,'limit':limit
        }
    response=get(url=url,params=param)
    try:
        out=read_json(response.text)
    except:
        raise Exception(response.text)
    #表格命名
    out.columns=['open_time','open','high','low','close','amount',
                 '','volume']
    #更改时间位数
    out['open_time']=out['open_time'].apply(lambda x:int(x/1000))
    return out

def sql_gate(symbol,interval,from_time,limit):
    #只接受大写
    symbol=symbol.upper()
    #发送请求
    url='https://api.gateio.ws/api/v4/spot/candlesticks'
    #设置to的大小
    if interval!='30d':
        if interval.find('m')!=-1:
            to_time=from_time+2*60*60
        elif interval.find('h')!=-1:
            to_time=from_time+2*24*60*60
        elif interval.find('d')!=-1:
            to_time=from_time+2*30*24*60*60
        param={
            'currency_pair':symbol,'interval':interval,
            'from':from_time,'to':to_time
            }
    else:
        param={
            'currency_pair':symbol,'interval':interval,'from':100000000
            }
    
    response=get(url=url,params=param)
    try:
        out=read_json(response.text)
    except:
        raise Exception(response.text)
    #表格命名
    try:
        out.columns=['open_time','volume','close',
                     'high','low','open','amount']
    except:
        #不能命名说明是空的，返回0
        out=DataFrame([[0,0,0,0,0,0,0]],columns=['open_time',
               'volume','close','high','low','open','amount'])
    return out

def sql_ftx(symbol,interval,from_time,limit):
    #只接受大写
    symbol=symbol.upper()
    #发送请求
    if str(interval)=='2592000':
        url='https://ftx.com/api/markets/'+str(symbol)+\
            '/candles?resolution='+str(interval)+\
            '&start_time='+str(from_time)
    else:
        url='https://ftx.com/api/markets/'+str(symbol)+\
            '/candles?resolution='+str(interval)+\
            '&start_time='+str(from_time)+\
            '&end_time='+str(int(from_time)+32*int(interval))
    response=get(url=url)
    try:
        out=DataFrame(list(read_json(response.text)['result']))
        #重命名
        out.columns=['','open_time','open','high','low','close','volume']
        #更改时间格式
        out['open_time']=out['open_time'].apply(lambda x:int(int(x)/1000))
    except:
        raise Exception(response.text)
    return out

def sql_bitget(symbol,interval,from_time,limit):
    #只接受大写
    symbol=symbol.upper()
    #调整时间
    from_time=str(int(from_time)*1000)
    #发送请求
    url='https://api.bitget.com/api/mix/v1/market/candles'
    #发送请求
    if str(interval)=='2592000':
        param={
            'symbol':symbol,'granularity':'604800',
            'startTime':from_time,'endTime':'9999999999999'
            }
    else:
        param={
            'symbol':symbol,'granularity':interval,
            'startTime':from_time,
            'endTime':str(int(from_time)+32*int(interval)*1000)
            }
    response=get(url=url,params=param)
    try:
        out=read_json(response.text)
    except:
        raise Exception(response.text)
    #表格命名
    try:
        out.columns=['open_time','open',
                     'high','low','close','amount','volume']
        #更改时间格式
        out['open_time']=out['open_time'].apply(lambda x:int(int(x)/1000))
    except:
        #不能命名说明是空的，返回0
        out=DataFrame([[0,0,0,0,0,0,0]],columns=['open_time','open',
                     'high','low','close','amount','volume'])
    return out

def sql_bybit(symbol,interval,from_time,limit):
    #只接受大写
    symbol=symbol.upper()
    url='https://api-testnet.bybit.com/v2/public/kline/list'
    param={
        'symbol':symbol,'interval':interval,'from':from_time,'limit':limit
        }
    response=get(url=url,params=param)
    try:
        out=DataFrame(list(read_json(response.text)['result']))
    except:
        raise Exception(response.text)
    return out


#查询并整理为dataframe格式
def sql(exchange,symbol,interval,from_time,limit):
    
    if exchange=='binance':
        return sql_binance(symbol,interval,from_time,limit)
    
    elif exchange=='huobi':
        return sql_huobi(symbol,interval,from_time,limit)
    
    elif exchange=='okx':
        return sql_okx(symbol,interval,from_time,limit)
    
    elif exchange=='mexc':
        return sql_mexc(symbol,interval,from_time,limit)
    
    elif exchange=='gate':
        return sql_gate(symbol,interval,from_time,limit)

    elif exchange=='ftx':
        return sql_ftx(symbol,interval,from_time,limit)

    elif exchange=='bitget':
        return sql_bitget(symbol,interval,from_time,limit)
    
    elif exchange=='bybit':
        return sql_bybit(symbol,interval,from_time,limit)


def choose_interval(exchange):
    if exchange=='binance':
        time_type=['1m','5m','15m','1h','1d','1w','1M']
    elif exchange=='huobi':
        time_type=['1min','5min','15min','60min','1day','1week','1mon']
    elif exchange=='okx':
        time_type=['1m','5m','15m','1H','1D','1W','1M']
    elif exchange=='mexc':
        time_type=['1m','5m','15m','60m','1d','1M','1M']
    elif exchange=='gate':
        time_type=['1m','5m','15m','1h','1d','7d','30d']
    elif exchange=='ftx':
        time_type=['60','300','900','3600','86400','604800','2592000']
    elif exchange=='bitget':
        time_type=['60','300','900','3600','86400','604800','2592000']
    elif exchange=='bybit':
        time_type=['1','5','15','60','D','W','M']
    return time_type

def calculate(prox,exchange,symbol):
    #设置代理
    environ["http_proxy"] = prox
    environ["https_proxy"] = prox
    #数据储存字典
    dic={'币种':symbol,'交易所':exchange}
    
    time_type=choose_interval(exchange)
    
    
    #查询最高价最低价
    response=sql(exchange,symbol,time_type[6],1,200)
    #查询最大值所在位置
    index=response['high'].apply(float).idxmax()
    #得到历史最高价
    dic['历史最高价']=response.iloc[index,:].loc['high']
    #再次查询这期间最大值所在天
    temp=sql(exchange,symbol,time_type[4],response['open_time'][index],32)
    #查询最大值所在位置
    index=temp['high'].apply(float).idxmax()
    
    dic['历史最高价时间']=strftime("%Y-%m-%d",
                            localtime(temp['open_time'][index]))
    
    #查询最小值所在位置
    index=response['low'].apply(float).idxmin()
    #得到历史最低价
    dic['历史最低价']=response.iloc[index,:].loc['low']
    temp=sql(exchange,symbol,time_type[4],response['open_time'][index],32)
    #查询最小值所在位置
    index=temp['low'].apply(float).idxmin()
    
    dic['历史最低价时间']=strftime("%Y-%m-%d",
                            localtime(temp['open_time'][index]))
    #目前币价
    dic['开盘价']=response.iloc[0,:].loc['open']
    dic['目前币价']=response.iloc[-1,:].loc['close']
    
    
    #第一月的数据
    dic['1月交易总额']=float(response['volume'][0])
    dic['1月回撤']=float(response['high'][0])-float(response['close'][0])
    dic['1月涨幅']=float(response['close'][0])-float(response['open'][0])
    
    
    #第一月的开盘时间
    from_time=int(response['open_time'][0])-1
    #对应的数据
    #倒着查询，从而逐步获得精确的开市时间
    key_type=['1分钟涨幅','1分钟回撤','1分钟的交易总额','5分钟涨幅','5分钟回撤',
     '5分钟的交易总额','15分钟涨幅','15分钟回撤','15分钟的交易总额','1小时涨幅',
     '1小时回撤','1小时交易总额','1日涨幅','1日回撤','1日交易总额','1周涨幅',
     '1周回撤','1周交易总额']
    #循环查询填入
    for i in range(len(time_type)-2,-1,-1):
        temp=sql(exchange,symbol,time_type[i],from_time,1)
        dic[key_type[3*i]]=float(temp['close'][0])-float(temp['open'][0])
        dic[key_type[3*i+1]]=float(temp['high'][0])-float(temp['close'][0])
        dic[key_type[3*i+2]]=float(temp['volume'][0])
        #查询的时间如果不为0，那么选择更详细的时间
        if temp['open_time'][0]!=0:
            from_time=temp['open_time'][0]-1
    
    output(dic,'币种查询储存.csv')
    print(dic)
    return dic


#主程序
def main():
    
    #主程序部分
    top = Tk()

    #文字
    Label(top,text='HTTP代理地址为xiyouVPN界面的右上角\n'+
                  '鼠标移动到信号标志上面后可以看到')\
        .grid(row=2, column=5)
        
    Label(top,text='此处输入要查询的交易符号\n'+
                  '具体交易符号要遵循相应交易所的习惯\n'+\
                  '如binance,huobi,mexc为BTCUSDT\n'+\
                  'okx为BTC-USDT,gate为BTC_USDT\n'+\
                  'ftx为BTC/USD,bitget为BTCUSDT_UMCBL\n'+\
                  'bybit为BTCUSD').grid(row=4, column=5)    
        
    Label(top,text='点击后需等待数秒\n'+
                  '当屏幕出现结果时说明查询成功\n'+\
                  '数据会保存在 币种查询储存.csv').grid(row=5, column=5)
        
    Label(top,text="HTTP代理地址").grid(row=2,column=0)
    Label(top,text="交易所").grid(row=3,column=0)
    Label(top,text="交易符号").grid(row=4,column=0)

    #输入框
    E1=Entry(top,bd=1)
    E1.grid(row=2,column=3)
    E1.insert(0,"http://127.0.0.1:9999")
    
    E2=ttk.Combobox(top)
    E2.grid(row=3,column=3)
    E2['value']=('binance','huobi','okx','mexc','gate','ftx','bitget','bybit')

    E3=Entry(top,bd=1)
    E3.grid(row=4,column=3)
    
    #按钮    
    Button(top, text ="查询信息",command=lambda:calculate\
                   (E1.get(),E2.get(),E3.get())).grid(row=5, column=3)

    top.mainloop()

main()


#设置代理
#number='10001'
#os.environ["http_proxy"] = "http://127.0.0.1:"+number
#os.environ["https_proxy"] = "http://127.0.0.1:"+number


#dic=calculate("http://127.0.0.1:10001",'binance','BTCUSDT')
#dic=calculate("http://127.0.0.1:10001",'huobi','btcusdt') 
#dic=calculate("http://127.0.0.1:10001",'okx','BTC-USDT')
#mexc的周数据无法得到，mexc自己的问题
#dic=calculate("http://127.0.0.1:10001",'mexc','BTCUSDT')  
#dic=calculate("http://127.0.0.1:10001",'gate','BTC_USDT')
#dic=calculate("http://127.0.0.1:10001",'ftx','BTC/USD')
#bitget没有月度数据，api自己就没有
#dic=calculate("http://127.0.0.1:10001",'bitget','BTCUSDT_UMCBL') 
#dic=calculate("http://127.0.0.1:10001",'bybit','BTCUSD')


