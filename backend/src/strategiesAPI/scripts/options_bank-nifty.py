import time
from alice_blue import *
import dateutil.parser
import datetime
import pandas as pd
import pandasql as ps
import requests
import openpyxl
import re
import django
django.setup()
from ..models import Papertrade
from optionchain.models import LTP

traded_stocks = []
instrument_list = ['Nifty Bank','Nifty 50']


session_id = AliceBlue.login_and_get_sessionID(username=username,
                                                    password=password,
                                                    twoFA=twoFA,
                                                    api_secret=api_secret,
                                                    app_id=app_id)
alice = AliceBlue(username=username,
                      session_id=session_id)

df_historical = pd.DataFrame()


def get_historical(instrument,
                   from_datetime,
                   to_datetime,
                   interval,
                   indices=False):
    params = {
        "token":
            instrument.token,
        "exchange":
            instrument.exchange if not indices else "NSE_INDICES",
        "starttime":
            str(int(from_datetime.timestamp())),
        "endtime":
            str(int(to_datetime.timestamp())),
        "candletype":
            3 if interval.upper() == "DAY" else
            (2 if interval.upper().split("_")[1] == "HR" else 1),
        "data_duration":
            None if interval.upper() == "DAY" else interval.split("_")[0]
    }
    lst = requests.get(f" https://ant.aliceblueonline.com/api/v1/charts/tdv?",
                       params=params).json()["data"]["candles"]
    records = []
    for i in lst:
        record = {
            "date": dateutil.parser.parse(i[0]),
            "open": i[1],
            "high": i[2],
            "low": i[3],
            "close": i[4]
        }
        records.append(record)
    return records


def test(i):
    instrument = alice.get_instrument_by_symbol("NSE", i)
    date = datetime.datetime.strptime('2017-05-04', "%Y-%m-%d")
    date_start = date.replace(minute=15,
                              hour=9,
                              second=00,
                              year=datetime.datetime.now().year,
                              month=datetime.datetime.now().month,
                              day=datetime.datetime.now().day)
    date_end = date.replace(minute=30,
                            hour=9,
                            second=00,
                            year=datetime.datetime.now().year,
                            month=datetime.datetime.now().month,
                            day=datetime.datetime.now().day)
    from_datetime = date_start - datetime.timedelta(
        days=0)
    to_datetime = date_end - datetime.timedelta(
        days=0)
    interval1 = "15_MIN"  # ["DAY", "1_HR", "3_HR", "1_MIN", "5_MIN", "15_MIN", "60_MIN"]
    indices = True
    df1 = pd.DataFrame(
        get_historical(instrument, from_datetime, to_datetime, interval1,
                       indices))

    q1 = """SELECT high FROM df1 order by high DESC LIMIT 1 """
    q2 = """SELECT low FROM df1 order by low ASC LIMIT 1 """
    s1 = ps.sqldf(q1, locals())
    s2 = ps.sqldf(q2, locals())

    high = s1["high"][0]
    low = s2["low"][0]

    return high,low


def test_fno(i):
    instrument = alice.get_instrument_by_symbol("NFO", i)
    date = datetime.datetime.strptime('2017-05-04', "%Y-%m-%d")
    date_start = date.replace(minute=15,
                              hour=9,
                              second=00,
                              year=datetime.datetime.now().year,
                              month=datetime.datetime.now().month,
                              day=datetime.datetime.now().day)
    date_end = date.replace(minute=30,
                            hour=9,
                            second=00,
                            year=datetime.datetime.now().year,
                            month=datetime.datetime.now().month,
                            day=datetime.datetime.now().day)
    from_datetime = date_start - datetime.timedelta(
        days=0)
    to_datetime = date_end - datetime.timedelta(
        days=0)
    interval1 = "15_MIN"  # ["DAY", "1_HR", "3_HR", "1_MIN", "5_MIN", "15_MIN", "60_MIN"]
    indices = False
    df1 = pd.DataFrame(
        get_historical(instrument, from_datetime, to_datetime, interval1,
                       indices))

    q1 = """SELECT high FROM df1 order by high DESC LIMIT 1 """
    q2 = """SELECT low FROM df1 order by low ASC LIMIT 1 """
    s1 = ps.sqldf(q1, locals())
    s2 = ps.sqldf(q2, locals())

    high = s1["high"][0]
    low = s2["low"][0]

    return high,low


def main():
    global df_historical
    # noinspection PyGlobalUndefined
    global algotrade_username

    high_bank,low_bank = test("Nifty Bank")
    high_fifty,low_fifty=test("Nifty 50")
    high_bank=(int)(high_bank/100)*100
    low_bank=(int)(low_bank/100)*100
    high_fifty=(int)(high_fifty/100)*100
    low_fifty=(int)(low_fifty/100)*100
    
    # To get weekly expiry
    df = pd.DataFrame(alice.search_instruments('NFO', 'BANKNIFTY'))
    df = df.filter(['expiry'])  # Filter only expiry dates
    df.drop_duplicates(inplace=True)  # keeping unique values
    df = df.sort_values(by=['expiry'], ascending=True)
    arr = df.to_numpy()  # Converts it to a 2D array of size n x 1
    
    bank_ce = alice.get_instrument_for_fno(symbol='BANKNIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=low_bank,
                                            is_CE=True).symbol
    bank_pe = alice.get_instrument_for_fno(symbol='BANKNIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=high_bank,
                                            is_CE=False).symbol
    nifty_ce = alice.get_instrument_for_fno(symbol='NIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=low_fifty,
                                            is_CE=True).symbol
    nifty_pe = alice.get_instrument_for_fno(symbol='NIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=high_fifty,
                                            is_CE=False).symbol                                                                                                                    
    high_bank_PE,low_bank_PE = test_fno(bank_pe)
    high_bank_CE,low_bank_CE = test_fno(bank_ce)
    high_fifty_PE,low_fifty_PE = test_fno(nifty_pe)
    high_fifty_CE,low_fifty_CE = test_fno(nifty_ce)

    Option_Chain=[bank_pe,bank_ce,nifty_pe,nifty_ce]

    while datetime.datetime.now().time() < datetime.time(9, 30, 00):
        pass

    interval = 60 - datetime.datetime.now().second
    time.sleep(interval + 2)

    while datetime.time(9, 31, 0) <= datetime.datetime.now().time() <= datetime.time(15, 0, 0):
        start = time.time()
        print(f'Option at {datetime.datetime.now().time().strftime("%H:%M")}')
        for x in Option_Chain:
            name = x
            if (name not in traded_stocks):
                traded_stocks.append(name)
                is_ce=False
                square_off=40.0
                stop_loss=30.0
                if(name==Option_Chain[0]):
                    symbol='BANKNIFTY'
                    hi=high_bank_PE
                    strike=high_bank
                    p = hi + 25
                elif(name==Option_Chain[1]):
                    symbol='BANKNIFTY'
                    hi=high_bank_CE
                    strike=low_bank
                    is_ce=True
                    p = hi + 25
                elif(name==Option_Chain[2]):
                    # symbol='NIFTY'
                    # hi=high_fifty_PE
                    # strike=high_fifty
                    # square_off=15.0
                    # stop_loss=15.0
                    # p = hi + 15
                    continue
                elif(name==Option_Chain[3]):
                    # symbol='NIFTY'
                    # hi=high_fifty_CE
                    # strike=low_fifty
                    # is_ce=True
                    # square_off=15.0
                    # stop_loss=15.0
                    # p = hi + 15
                    continue
                print(f"Entry {name} {hi}")
                
                alice.place_order(transaction_type=TransactionType.Buy,
                                  instrument=alice.get_instrument_for_fno(symbol = symbol, 
                                  expiry_date=arr[0][0], is_fut=False, strike=strike, is_CE = is_ce),
                                  quantity=25,
                                  order_type=OrderType.StopLossLimit,
                                  product_type=ProductType.Intraday,
                                  price=(float)(p),
                                  trigger_price=(float)(p),
                                  stop_loss=(float)(stop_loss),
                                  square_off=(float)(square_off),
                                  trailing_sl=None,
                                  is_amo= False)
              
      
        interval = 60 - time.time() + start
        time.sleep(interval)



def start_paper_trade():
    global df_historical
    # noinspection PyGlobalUndefined
    global algotrade_username

    high_bank,low_bank = test("Nifty Bank")
    high_fifty,low_fifty=test("Nifty 50")
    high_bank=(int)(high_bank/100)*100
    low_bank=(int)(low_bank/100)*100
    high_fifty=(int)(high_fifty/100)*100
    low_fifty=(int)(low_fifty/100)*100

    df = pd.DataFrame(alice.search_instruments('NFO', 'BANKNIFTY'))
    df = df.filter(['expiry'])  # Filter only expiry dates
    df.drop_duplicates(inplace=True)  # keeping unique values
    df = df.sort_values(by=['expiry'], ascending=True)
    arr = df.to_numpy()  # Converts it to a 2D array of size n x 1
    
    bank_ce = alice.get_instrument_for_fno(symbol='BANKNIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=low_bank,
                                            is_CE=True).symbol
    bank_pe = alice.get_instrument_for_fno(symbol='BANKNIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=high_bank,
                                            is_CE=False).symbol
    nifty_ce = alice.get_instrument_for_fno(symbol='NIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=low_fifty,
                                            is_CE=True).symbol
    nifty_pe = alice.get_instrument_for_fno(symbol='NIFTY',
                                            expiry_date=arr[0][0],
                                            is_fut=False,
                                            strike=high_fifty,
                                            is_CE=False).symbol                                                                                                                    
    high_bank_PE,low_bank_PE = test_fno(bank_pe)
    high_bank_CE,low_bank_CE = test_fno(bank_ce)
    high_fifty_PE,low_fifty_PE = test_fno(nifty_pe)
    high_fifty_CE,low_fifty_CE = test_fno(nifty_ce)

    Option_Chain=[bank_pe,bank_ce,nifty_pe,nifty_ce]

    while datetime.datetime.now().time() < datetime.time(9, 30, 00):
        pass

    interval = 60 - datetime.datetime.now().second
    time.sleep(interval + 2)

    while datetime.time(9, 31, 0) <= datetime.datetime.now().time() <= datetime.time(15, 0, 0):
        start = time.time()
        print(f'Option at {datetime.datetime.now().time().strftime("%H:%M")}')
        for x in Option_Chain:
            name = x
            if (name not in traded_stocks):
                traded_stocks.append(name)
                square_off=40.0
                stop_loss=30.0
                if(name==Option_Chain[0]):
                    hi=high_bank_PE
                    p = hi + 25
                elif(name==Option_Chain[1]):
                    hi=high_bank_CE
                    p = hi + 25
                elif(name==Option_Chain[2]):
                    # symbol='NIFTY'
                    # hi=high_fifty_PE
                    # strike=high_fifty
                    # square_off=20.0
                    # stop_loss=15.0
                    # p = hi + 15
                    continue
                elif(name==Option_Chain[3]):
                    # symbol='NIFTY'
                    # hi=high_fifty_CE
                    # strike=low_fifty
                    # is_ce=True
                    # square_off=20.0
                    # stop_loss=15.0
                    # p = hi + 15
                    continue
                print(f"Entry {name} {hi}")
                Papertrade.objects.create(start_time=datetime.datetime.now().time().strftime("%H:%M"),username=algotrade_username, signal='BUY', name=name, quantity=25,
                                    buy_price=p, sell_price=0, stop_loss=p-stop_loss, target=square_off,net_charges=200,Invested=(hi+25)*100)

              
      
        interval = 60 - time.time() + start
        time.sleep(interval)
