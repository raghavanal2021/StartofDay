import pymssql
from datetime import datetime, timedelta
import pandas as pd
class EndofDayFeed(object):
    
    ''' Initialize the Database connection '''
    def __init__(self):
        self.conn = pymssql.connect(server='localhost',user='tradedev',password='tradedev',database='TradeRepository')
        
        
    ''' Get the Data for the day '''    
    def getData(self,target, noofdays):
        endDate = target
        startDate = datetime.strftime(datetime.strptime(target,'%Y%m%d') - timedelta(days=noofdays),'%Y%m%d')
        cursor = self.conn.cursor()
        query = 'SELECT symbol, tradedate,openPrice,highPrice,lowPrice,closePrice,volume FROM t_eod_equities_data WHERE tradeDate between %(start)s and %(end)s'
        df = pd.read_sql(query,params={"start":startDate,"end":endDate},con=self.conn)
        df['timestamp'] = pd.to_datetime(df['tradedate'],format='%Y%m%d',errors='ignore')
        df = df.set_index(df['timestamp'])
        return df
    
    