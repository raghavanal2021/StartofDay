import pymssql
from datetime import datetime, timedelta
import pandas as pd
class EndofDayFeedSymbol(object):
    
    ''' Initialize the Database connection '''
    def __init__(self):
        self.conn = pymssql.connect(server='localhost',user='tradedev',password='tradedev',database='TradeRepository')
        
        
    ''' Get the Data for the day '''    
    def getData(self,symbol ,target, noofdays):
        endDate = target
        startDate = datetime.strftime(datetime.strptime(target,'%Y%m%d') - timedelta(days=noofdays),'%Y%m%d')
        cursor = self.conn.cursor()
        query = 'SELECT symbol, tradedate,openPrice,highPrice,lowPrice,closePrice,volume FROM t_eod_equities_data WHERE symbol = %(symbol)s tradeDate between %(start)s and %(end)s'
        df = pd.read_sql(query,params={"symbol":symbol,"start":startDate,"end":endDate},con=self.conn)
        df['timestamp'] = pd.to_datetime(df['tradedate'],format='%Y%m%d',errors='ignore')
        df = df.set_index(df['timestamp'])
        return df
    
    
    def getMaster(self):
        query = "SELECT distinct master_symbol,master_name,master_isin FROM t_equities_master a INNER JOIN t_indices_stocks_map b on a.master_symbol = b.symbol"
        masterdf = pd.read_sql(query,self.conn)
        return masterdf
        