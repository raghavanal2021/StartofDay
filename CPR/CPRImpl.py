from DataFeed.Feed import EndofDayFeed
import pandas as pd
import talib as tl
import numpy as np
from datetime import datetime
from pymongo import MongoClient

class CPRImplementation:
    
    pivotpoints = pd.DataFrame()
    
    def __init__(self,target,noofdays):
        self.feed = EndofDayFeed().getData(target=target, noofdays=noofdays+20)
        self.target = target
    
    def pivotCalculation(self):
        df = self.feed
        df['prevopen'] = df['openPrice'].shift(1)
        df['prevhigh'] = df['highPrice'].shift(1)
        df['prevlow']  = df['lowPrice'].shift(1)
        df['prevclose'] = df['closePrice'].shift(1)
        df['prevVolume'] = df['volume'].shift(1)
        self.pivotpoints['prevhigh'] = df['prevhigh']
        self.pivotpoints['prevlow'] = df['prevlow']
        self.pivotpoints['prevclose'] = df['prevclose']
        self.pivotpoints['prevVolume'] = df['prevVolume']
        self.pivotpoints['symbol'] = df['symbol']
        self.pivotpoints['timestamp'] =pd.to_datetime(df['tradedate'],format='%Y%m%d',errors='ignore')
        self.pivotpoints['pivot'] = round((df['prevhigh']+df['prevlow']+df['prevclose'])/3.0,2)
        self.pivotpoints['BC'] = round((df['prevhigh']+df['prevlow'])/2,2)
        self.pivotpoints['TC'] = round((self.pivotpoints['pivot'] - self.pivotpoints['BC']) + self.pivotpoints['pivot'],2)
        self.pivotpoints['width'] = (abs(self.pivotpoints['BC'] - self.pivotpoints['TC'])/self.pivotpoints['pivot'])*100
        widthdf = self.pivotpoints.groupby(['symbol'])['width'].mean().to_frame('averagewidth').reset_index()
        widthdf = widthdf.rename(columns={'symbol':'symbol_width','averagewidth':'averagewidth'})
        self.pivotpoints = pd.merge(self.pivotpoints,widthdf,left_on="symbol",right_on="symbol_width")
        self.pivotpoints.loc[self.pivotpoints['width'] < (80/100)*self.pivotpoints['averagewidth'],'WidthShape'] = 'Narrow'
        self.pivotpoints.loc[self.pivotpoints['width'] > (120/100)*self.pivotpoints['averagewidth'],'WidthShape'] = 'Broad'
        return self.pivotpoints
    
    def camarillapoints(self,df):
        self.pivotpoints['R1'] = round(((df['prevhigh'] - df['prevlow'])*1.1/12 + df['prevclose']),2)
        self.pivotpoints['R2'] = round(((df['prevhigh'] - df['prevlow'])*1.1/6 + df['prevclose']),2)
        self.pivotpoints['R3'] = round(((df['prevhigh'] - df['prevlow'])*1.1/4 + df['prevclose']),2)
        self.pivotpoints['R4'] = round(((df['prevhigh'] - df['prevlow'])*1.1/2 + df['prevclose']),2)
        self.pivotpoints['S1'] = round((df['prevclose'] - ((df['prevhigh'] - df['prevlow'])*1.1/12)),2)
        self.pivotpoints['S2'] = round((df['prevclose'] - ((df['prevhigh'] - df['prevlow'])*1.1/6)),2)
        self.pivotpoints['S3'] = round((df['prevclose'] - ((df['prevhigh'] - df['prevlow'])*1.1/4)),2)
        self.pivotpoints['S4'] = round((df['prevclose'] - ((df['prevhigh'] - df['prevlow'])*1.1/2)),2)
        return self.pivotpoints
    
    def fibonaccipoints(self):
        df = self.feed
        self.pivotpoints['FibR1'] = round(self.pivotpoints['pivot'] + ((df['prevhigh'] - df['prevlow'])*0.382),2)
        self.pivotpoints['FibR2'] = round(self.pivotpoints['pivot'] + ((df['prevhigh'] - df['prevlow'])*0.618),2)
        self.pivotpoints['FibR3'] = round(self.pivotpoints['pivot'] + ((df['prevhigh'] - df['prevlow'])*0.786),2)
        self.pivotpoints['FibR4'] = round(self.pivotpoints['pivot'] + ((df['prevhigh'] - df['prevlow'])*1.000),2)
        self.pivotpoints['FibS1'] = round(self.pivotpoints['pivot'] - ((df['prevhigh'] - df['prevlow'])*0.382),2)
        self.pivotpoints['FibS2'] = round(self.pivotpoints['pivot'] - ((df['prevhigh'] - df['prevlow'])*0.618),2)
        self.pivotpoints['FibS3'] = round(self.pivotpoints['pivot'] - ((df['prevhigh'] - df['prevlow'])*0.786),2)
        self.pivotpoints['FibS4'] = round(self.pivotpoints['pivot'] - ((df['prevhigh'] - df['prevlow'])*1.000),2)
        return self.pivotpoints
    
    def returnlatest(self,target):
        startDate = datetime.strptime(target,'%Y%m%d')
        df =self.pivotpoints[(self.pivotpoints['timestamp'] == startDate)]
        #df.to_csv("test.csv")
        #print(df)
        outputdf = df[df['WidthShape'] == 'Narrow']
        outputdict = {"name":"cpr","data":outputdf.to_json(orient='records',date_format='iso')}
        self.client = MongoClient('localhost',27017)
        self.db = self.client["StartofDay"]
        self.coll = self.db[self.target]
        self.coll.remove({"name":"cpr"})
        self.coll.insert(outputdict)
        return outputdf
        
        
    