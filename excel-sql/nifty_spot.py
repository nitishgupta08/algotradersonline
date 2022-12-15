'''Ths Module exports NIFTY excel to SQL'''
from time import sleep
from sqlalchemy import create_engine
from config import Credentials
import xlwings as xw
import pandas as pd
import datetime as dt


def connect_to_sql():
    '''Returns SQL object'''
    print(Credentials.USERNAME.value)
    my_conn = create_engine(f"mysql+mysqldb://{Credentials.USERNAME.value}:{Credentials.PASSWORD.value}@{Credentials.IP.value}/{Credentials.DB_NAME.value}")
    print(my_conn)
    return my_conn

def live_to_excel(my_conn):
    '''Reads live excel data and exporting it to sql every second'''
    wrbk = xw.Book('option_chain.xlsx')
    nitfty_sheet = wrbk.sheets['NIFTY']
    
    live_data = {
        'id':[1,2,3],
        'name': [nitfty_sheet['B3'].value,nitfty_sheet['B4'].value,nitfty_sheet['J3'].value],
        'ltp':[nitfty_sheet['D3'].value, nitfty_sheet['D4'].value,nitfty_sheet['J4'].value],
        'chn_prev_day':[nitfty_sheet['E3'].value,nitfty_sheet['E4'].value, None],
        'per_chn':[nitfty_sheet['F3'].value,nitfty_sheet['F4'].value,None],
        'oi_per_chn':[None,nitfty_sheet['G4'].value,None]
    }
    
    live_df = pd.DataFrame(live_data)
    live_df.to_sql(con=my_conn,name="optionchain_ltp",if_exists="replace",index=False)
    print(f"Live data updated to database at {dt.datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    db_conn = connect_to_sql()
    while(True):
        live_to_excel(db_conn)
        sleep(1)


