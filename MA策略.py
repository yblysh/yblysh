# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 08:13:44 2022

@author: WIN10
"""

import pandas as pd
from stockstudy import get_stock,localgetdf,calculate,returns_plot,tsgetdf
import matplotlib.pyplot as plt
from math import log
import csv
import os

#MA计算,从1到time全部计算
def MAcreate(df,n,days):
    ma=df.copy()
    ma=ma.iloc[-days-n-10:,:]
    ma['hl']=(ma.high+ma.low)/2
    for i in range(1,n+1):
        x=ma['close'].rolling(i).mean().shift(1)
        ma.loc[:,i]=x
    ma=ma.dropna()
    return ma

#MA计算,只计算指定的time
def MAcreate2(df,n,days):
    ma=df.copy()
    ma=ma.iloc[-days-n-10:,:]
    ma['hl']=(ma.high+ma.low)/2
    for i in [n]:
        x=ma['close'].rolling(i).mean().shift(1)
        ma.loc[:,i]=x
    ma=ma.dropna()
    return ma

#绘制成功、失败图，成功+1失败-1
def returns_plot2(predict,changelist,n,p):
    predict=predict[:-1]
    #计算出手回报
    incomeList=[]
    #出手收益
    returns=0
    for i in range(len(predict)):
        change=changelist.iloc[i]
        #大于指示则买入，并计算收益
        if predict[i]>p:
            if change>1:
                returns+=1
            else:
                returns+=-1
        #计算以来的收益率
        incomeList.append(returns)
    
    plt.plot(incomeList)
    plt.text(0,0,n)
    plt.show()

#计算单次回报，不进行累加
def returns_cal(predict,changelist,n,p):
    predict=list(predict[:-1])
    #计算回报
    incomeList=[]
    for i in range(len(predict)):
        change=changelist.iloc[i]
        #大于指示则买入，并计算收益
        if predict[i]>p:
            incomeList.append(log(change))
        else:
            incomeList.append(0)
    return incomeList

#获得预测列表
def get_pred(ma,n,days):
    predict=[]
    for i in range(days):
        #昨日最高价小于n阶ma；今日最高价高于n阶ma
        r1=1
        r2=1/r1
        if ma['hl'].iloc[-days+i-1]<ma[n].iloc[-days+i-1]*r1 and ma['hl'].iloc[-days+i]>ma[n].iloc[-days+i]*r2: 
        #if ma['low'].iloc[-days+i-1]<ma[n].iloc[-days+i-1]*r1 and ma['low'].iloc[-days+i]>ma[n].iloc[-days+i]*r2: 
            predict.append(1)
        else:
            predict.append(-1)
    return predict


#2000天内选择最佳策略
#situation=0时强制进行参数搜索，=1时如果dic有参数记录则选用，没有则参数搜索
def filt(df,stock,dic,situation=0):
    days=400
    #如果股票较新
    if len(df)<days+50:
        days=len(df)-60
    if stock in dic.index and situation:
        #n取值范围
        ran=[int(dic.loc[stock][0])]
        #创立ma数据库
        ma=MAcreate2(df,int(dic.loc[stock][0]),days)
    else:
        ran=range(1,50)
        ma=MAcreate(df,50,days)
    returnList=pd.DataFrame(columns=[])
    predictList=pd.DataFrame(columns=[])
    for n in ran:
        #建立预测列表
        predict=get_pred(ma,n,days)
        predictList[n]=pd.Series(predict)
        returns=calculate(predict,
        (df['close']*0.9965/df['close'].shift(1)*1.0025).iloc[-days+1:],n,0)
        returnList=pd.concat((returnList,returns))

    try:
        returnList['得分']=returnList['日回报率']
        returnList=returnList.sort_values('得分',ascending=False)
        n_choose=returnList.index[0]
        print("'"+stock+"':"+str(n_choose)+',')
        returns=calculate(predictList[n_choose],
    (df['close']*0.9965/df['close'].shift(1)*1.0025).iloc[-days+1:],
    n_choose,0)
        #returns_plot(predictList[n_choose],
    #(df['close']*0.9965/df['close'].shift(1)*1.0025).iloc[-days+1:],stock,0)
        n_best=pd.DataFrame([[n_choose,returns['日回报率'].iloc[0],
                    returns['胜率'].iloc[0],returns['0.05胜率'].iloc[0],
                    returns['残差'].iloc[0]]],
                    columns=['n','日回报率','胜率','0.05胜率','残差'])
        n_best.index=[stock]
        return n_best,predictList[n_choose]
    except:
        print("'"+stock+"':"+'策略失效')
        return pd.DataFrame([['策略失效','','','','']],
                    columns=['n','日回报率','胜率','0.05胜率','残差']),[]


#任意天内，计算给定策略的预测值
def filt2(stock,dic,days):
    if stock in dic.index:
        #n取值范围
        n=int(dic.loc[stock][0])
        #创立ma数据库
        ma=MAcreate2(df,n,days)
    else:
        raise Exception()
    #建立预测列表
    predict=get_pred(ma,n,days)
    
    return predict

def total_income(incomedf):
    incomedf=incomedf.copy()
    #incomedf=incomedf[incomedf['得分']>0.5]
    #建立胜率列表
    v=incomedf['得分']
    v.index=range(len(incomedf))
    #建立收益矩阵
    incomeList=pd.DataFrame(list(incomedf.loc[:,'收益']))
    #对每个收益标注策略的胜率
    choose_income=[]
    for i in range(len(incomedf.iloc[0,1])):
        try:
            idx=incomedf['得分'][incomeList.iloc[:,i]!=0].idxmax()
            choose_income.append(incomeList.iloc[idx,i])
        except:
            choose_income.append(0)
    choose_income
    #累加
    total=pd.Series(choose_income).cumsum()
    plt.plot(total)
    return total

#%%
if __name__ == '__main__':
    incomedf=pd.DataFrame(columns=[])
    ndic=pd.DataFrame(columns=[])
    #codelist=list(os.walk('data'))[0][2]
    codelist=['600778']
    dic=pd.read_csv('参数储存.csv',index_col=0)
    dic.index=pd.read_csv('参数储存.csv',dtype=pd.StringDtype(),index_col=0).index
    
    for stock in codelist:
    #for stock in dic.index:
        if stock.find('.csv')!=-1:
            stock=stock[:-4]
        #从tushare调取数据
        #df=tsgetdf(get_stock(stock),'20100101')
        df=localgetdf('data/'+stock+'.csv')
        
        #situation决定要不要计算收益
        situation=0
        
        if situation==0:
            #计算过去n天的最佳策略，给出最佳的n
            try:
                n_best,predict=filt(df,stock,dic,0)
            except:
                continue
            if n_best['n'][0]=='策略失效':
                continue
            ndic=pd.concat((ndic,n_best))
        else:
            #给出指定天数的当前策略的预测值
            predict=filt2(stock,dic,200)
    #%%  
        ##得到收益曲线
        
        
        temp=returns_cal(predict,
    (df['close']*0.9965/df['close'].shift(1)*1.0025).iloc[-len(predict)+1:],0,0)
        income=pd.DataFrame([[dic.loc[stock]['胜率'],temp]],
                                columns=['得分','收益'])
        incomedf=pd.concat((incomedf,income))
            
        
        #写入
        #ndic.to_csv('参数储存.csv')
        
    #%%
    total=total_income(incomedf)
    
    #读取所有代码
    #a=pd.read_excel(r'C:\Users\WIN10\Desktop\Table2.xlsx',
    #       0,dtype=pd.StringDtype())
    #code=list(a['code'])



