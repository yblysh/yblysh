# -*- coding: utf-8 -*-

import multiprocessing
from sklearn import svm
import pandas as pd
import numpy as np
import time
from stockstudy import get_stock,tsgetdf,calculate,returns_plot
                                     


#创建数据
def creatdata(df1,n):
    x=[]
    df=df1.copy()
    #df.loc[:,'high-low']=df.loc[:,'high']+df.loc[:,'low']
    
    for i in range(len(df)):
        x.append([])
        for j in range(1,n):
            #x[i].append(df.loc[:,'high'].iloc[i-j]/df.loc[:,'high'].iloc[i])
            #x[i].append(df.loc[:,'low'].iloc[i-j]/df.loc[:,'low'].iloc[i])
            #x[i].append(df.loc[:,'open'].iloc[i-j]/df.loc[:,'open'].iloc[i])
            #x[i].append(df.loc[:,'close'].iloc[i-j]/df.loc[:,'close'].iloc[i])
            #x[i].append(df.loc[:,'high'].iloc[i-j]/df.loc[:,'low'].iloc[i])
            #x[i].append(df.loc[:,'low'].iloc[i-j]/df.loc[:,'high'].iloc[i])
            #x[i].append(df.loc[:,'open'].iloc[i-j]/df.loc[:,'close'].iloc[i])
            #x[i].append(df.loc[:,'high'].iloc[i-j]/df.loc[:,'close'].iloc[i])
            #x[i].append(df.loc[:,'low'].iloc[i-j]/df.loc[:,'close'].iloc[i])
            x[i].append(df.loc[:,'hl'].iloc[i-j]/df.loc[:,'hl'].iloc[i]-1)
            
    return pd.DataFrame(x[n:])

def createy(df1,indicator,n):
    df=df1.copy()
    #df.loc[:,'high-low']=df.loc[:,'high']+df.loc[:,'low']
    #让时间错开，从而预测
    y=[]
    for i in range(len(df)):
        y.append(df.loc[:,'hl'].iloc[i]/df.loc[:,'hl'].iloc[i-1]-1)
    y=pd.Series(y[n+1:])

    #y=df.loc[:,'pct_chg'].iloc[n+1:]-1
    y=pd.concat((y,pd.Series(0)))
    #y转换为int
    #y=y.apply(lambda x:int(x*1000))
    y=y.apply(lambda x:1 if x>indicator else -1)
    
    return y


#逐步检验
def work(x,y,days,i):
    #创建模型
    model=svm.SVC()
    #model=create_LSTM()
    #model=RandomForestClassifier()
    #拟合模型
    model.fit(x[:i-days],y[:i-days])
    #model.fit(x[:i-days],y[:i-days],epochs=3)
    #得到结果
    result=model.predict([x.iloc[i-days,:]])[0]
    #result=model.predict([x.iloc[i-days,:]])[0][0]
    return (i,result)

def svm_pred(x,y,days,indicator):
    
    #进程池
    pool=multiprocessing.Pool(processes=6)

    #并行列表
    job_list=[]
    for i in range(days):
        #创建并行进程
        job_list.append(pool.apply_async(work,(x,y,days,i)))
        #开始进程
    pool.close()
    pool.join()
    result={}
    for p in job_list:
        #获得结果
        temp=p.get()
        #i对应的预测值
        result[temp[0]]=temp[1]
    predict=[]
    for i in range(days):
        predict.append(result[i])    
        
    return predict



#检验过去的
def work2(x,y,days,indicator):
    
    #创建模型
    model=svm.SVC()
    #拟合模型
    model.fit(x[:-days],y[:-days])
    #得到结果
    result=list(model.predict(x.iloc[-days:,:]))
    #result=list(model.predict(x.iloc[:-days,:]))
    return (indicator,result)


def svm_pred2(x,days,ran_i,df,n):
    #进程池
    pool=multiprocessing.Pool(processes=6)
    #并行列表
    job_list=[]
    for indicator in ran_i:
        #创建y
        y=createy(df,indicator,n)
        #创建并行进程
        job_list.append(pool.apply_async(work2,(x,y,days,indicator)))
        #开始进程
    pool.close()
    pool.join()
    result={}
    for p in job_list:
        #获得结果
        temp=p.get()
        #i对应的预测值
        result[temp[0]]=temp[1]
    returnList=pd.DataFrame(columns=[])
    #计算回报
    for i in ran_i:
        returns=calculate(result[i],df.loc[:,'hlc'].iloc[-days+1:],
                          str(n)+' '+str(round(i,7)),0)
        #returns=calculate(result[i],df.loc[:,'pct_chg'].iloc[n+1:-days+1],
        #                  str(n)+' '+str(round(i,7)),0)
        returnList=pd.concat((returnList,returns))

    return returnList

def prepare(stock,dic):
    if stock in dic and 0:
        #n取值范围
        ran=[dic[stock][0]]
        #y大于多少为1
        ran_i=[dic[stock][1]]
    else:
        ran=range(2,22)
        ran_i=np.arange(0,0.011,.0005)
    return ran,ran_i

if __name__ == '__main__':    
    
    dic={'600963':[6,0.01],'600778':[3,0.0035],'000100':[13,0.0055],
         '600010':[4,0.0065],'601398':[3,0.0015],'002208':[16,0.005],
         '002204':[6,0.004],'002607':[11,0.0045],'601828':[16,0.0045],
         '601015':[3,0.0075],'000158':[6,0.0025],'002563':[7,0.0017],
         '002658':[11,0.0028],'002269':[3,0.00]}
    #预测列表
    predictList=[]
    #结果列表
    returnList=pd.DataFrame(columns=[])
    for stock in ['600778']:
        print(stock)
    
        #stock='601398'
        #获得数据
        df=tsgetdf(get_stock(stock),'20130101')
        df=df.iloc[:-100,:]
        
        #准备工作
        ran,ran_i=prepare(stock,dic)
        
        days=400
        a=time.time()
        for n in ran:
            #创建x
            x=creatdata(df,n)
            
            if 0:
                returnList=pd.concat((returnList,svm_pred2(x,days,ran_i,df,n)))
            else:
                for indicator in ran_i:
                    #创建y
                    y=createy(df,indicator,n)
                    #进行预测
                    predict=svm_pred(x,y,days,indicator)
                    
                    #计算回报
                    returns=calculate(predict,df.loc[:,'hlc'].iloc[-days+1:],
                                      str(n)+' '+str(round(indicator,7)),0)
                    if returns['持仓时间'].iloc[0]==0:
                        break
                    #绘图
                    #returns_plot(predict,df.loc[:,'hlc'].iloc[-days+1:],
                    #             str(n)+' '+str(round(indicator,7)),0)
                    predictList.append(predict)
                    returnList=pd.concat((returnList,returns))
                
    
    
        b=time.time()
        print(b-a)






    


