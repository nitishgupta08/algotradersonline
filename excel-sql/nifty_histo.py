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


def export_to_sql(my_conn):
    '''Reads nifty excel file and exporting it to sql every minute'''
    wrbk = xw.Book('option_chain.xlsx')
    nitfty_sheet = wrbk.sheets['NIFTY']
    
    histo_df = nitfty_sheet.range("A6:V35").options(pd.DataFrame).value
    histo_df.reset_index(drop=True,inplace=True)
    histo_df.columns = [
        "Volume_C",
        "OI_Change_C",
        "OI_C",
        "LTP_C",
        "Strike_Price",
        "LTP_P",
        "OI_P",
        "OI_Change_P",
        "Volume_P",
        "PUT_CALL_OI_CHN",
        "PUT_CALL_OI",
        "PCR",
        "CPR",
        "STRONGNESS_OF_SUPPORT",
        "Reverse_Weightage",
        "Buy_Sell",
        "Stongness_Level",
        "Immediate_Support",
        "Strong_Support",
        "PCR_Weightage",
        "CPR_Weightage"
    ]
    histo_df['date_time'] = dt.datetime.utcnow().replace(second=0, microsecond=0)
    histo_df.to_sql(con=my_conn,name="optionchain_nifty_histo",if_exists="append",index=False)
    print(f"NIFTY historical updated to database at {dt.datetime.now().strftime('%H:%M:%S')}")
   
    


if __name__ == "__main__":
    db_conn = connect_to_sql()
    while(True):
        export_to_sql(db_conn)
        sleep(120)



