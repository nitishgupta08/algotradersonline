import time
from alice_blue import *
import dateutil.parser
import datetime
import pandas as pd
import pandasql as ps
import requests
import django
django.setup()
from ..models import Papertrade, OneMIN

traded_stocks = []
instrument_list = []


session_id = AliceBlue.login_and_get_sessionID(username=username,
                                                    password=password,
                                                    twoFA=twoFA,
                                                    api_secret=api_secret,
                                                    app_id=app_id)
alice = AliceBlue(username=username,
                      session_id=session_id)

# Get monthly expiry
df = pd.DataFrame(alice.search_instruments('NFO', 'BANKNIFTY'))
df = df.filter(['expiry'])  # Filter only expiry dates
df.drop_duplicates(inplace=True)  # keeping unique values
df = df.sort_values(by=['expiry'], ascending=True)
arr = df.to_numpy()  # Converts it to a 2D array of size n x 1
t = arr[0][0].month  # Getting the month of the first date
for i in range(0, len(arr)):
    if (arr[i][0].month > t):
        break
    date = arr[i][0]  # This will save the monthly expiry

bank = alice.get_instrument_for_fno(symbol = 'BANKNIFTY', expiry_date=date, is_fut=True, strike=None, is_CE = False).symbol
nifty=alice.get_instrument_for_fno(symbol = 'NIFTY', expiry_date=date, is_fut=True, strike=None, is_CE = False).symbol

instrument_list.append(bank)
instrument_list.append(nifty)

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
            "close": i[4],
            "volume": i[5]
        }
        records.append(record)
    return records


def test(i):
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

# def main():
#     global df_historical
#     for x in range(len(instrument_list)):
#         name = instrument_list[x]
#         vo = test(name)
#         data = {'symbol': name, 'volume': vo}
#         df_histo = pd.DataFrame(data, index=[x])
#         df_historical = pd.concat([df_historical, df_histo])
#         print(f"{df_historical['symbol'][x]}  {df_historical['volume'][x]} {x}")

#     while datetime.datetime.now().time() < datetime.time(9, 15, 00):
#         pass
#     # interval = (5 - datetime.datetime.now().minute % 5)*60 - (datetime.datetime.now().second)
#     interval = 60 - datetime.datetime.now().second
#     time.sleep(interval + 2)

#     while datetime.time(9, 16, 2) <= datetime.datetime.now().time() <= datetime.time(15, 25, 5):
#         start = time.time()
#         wrkbk = openpyxl.load_workbook(
#             f'/home/vmadmin/Desktop/algoTrade-main/backend/live_candle_data/{datetime.datetime.now().strftime("%Y-%m-%d")}_1MIN.xlsx')
#         wrkbk.active = wrkbk['Sheet1']
#         sh = wrkbk.active
#         rows_num = row_count(sh)
#         print(f'1MIN candle at {datetime.datetime.now().time().strftime("%H:%M")}')
#         x = rows_num - 81
#         for y in range(len(instrument_list)):
#             name = sh.cell(row=x, column=2).value
#             vo = df_historical['volume'][y]
#             vol = sh.cell(row=x, column=3).value
#             open = sh.cell(row=x, column=4).value
#             close = sh.cell(row=x, column=5).value
#             high = sh.cell(row=x, column=6).value
#             low = sh.cell(row=x, column=7).value
#             atp = sh.cell(row=x, column=9).value
#             range_oc2 = close - open
#             range_hl2 = high - low
#             range_hl1 = high - low
#             range_oc1 = open - close
#             money = 100000
#             l1 = low - low * 0.1 / 100
#             h1 = high + high * 0.1 / 100
#             quantity_b = int(money / h1)
#             quantity_s = int(money / l1)

#             if ((name not in traded_stocks) and (vol > vo) and (open < close)
#                     and (range_oc2 > range_hl2 * 0.80) and (close > atp)):
#                 traded_stocks.append(name)
#                 print(f"Entry {name} {vol} {vo}")
#                 alice.place_order(transaction_type=TransactionType.Buy,
#                                   instrument=alice.get_instrument_by_symbol(
#                                       'NSE', name),
#                                   quantity=quantity_b,
#                                   order_type=OrderType.Market,
#                                   product_type=ProductType.Delivery,
#                                   price=0.0,
#                                   trigger_price=None,
#                                   stop_loss=float(low),
#                                   square_off=float(2 * (high - low)),
#                                   trailing_sl=None,
#                                   is_amo=False)

#             if (name not in traded_stocks) and (vol > vo) and (open > close) and (range_oc1 > range_hl1 * 0.80) and (close < atp):
#                 print(f"Exit {name} {name} {vol} {vo}")
#                 traded_stocks.append(name)
#                 alice.place_order(transaction_type=TransactionType.Sell,
#                                   instrument=alice.get_instrument_by_symbol(
#                                       'NSE', name),
#                                   quantity=quantity_s,
#                                   order_type=OrderType.Market,
#                                   product_type=ProductType.Intraday,
#                                   price=0.0,
#                                   trigger_price=None,
#                                   stop_loss=float(low),
#                                   square_off=float(2 * (high - low)),
#                                   trailing_sl=None,
#                                   is_amo=False)
#             x += 1
#             wrkbk.close()
#         interval = 60 - (time.time() - start)
#         time.sleep(interval)


def start_paper_trade():
    # noinspection PyGlobalUndefined
    global algotrade_username
    for name in instrument_list:
        high,low = test(name)
        q = OneMIN.objects.get(name=name)
        q.historical_high = high
        q.historical_low = low
        q.save()
        
        print(f"{name}: high={high} low={low}")

    while datetime.datetime.now().time() < datetime.time(9, 30, 00):
        pass

    interval = 60 - datetime.datetime.now().second
    time.sleep(interval + 2)

    while datetime.time(9, 31, 0) <= datetime.datetime.now().time() <= datetime.time(15, 0, 0):
        start = time.time()
        print(f'FUTURES candle at {datetime.datetime.now().time().strftime("%H:%M")}')
        
        for name in instrument_list:
            q = OneMIN.objects.get(name=name)
            hi = q.historical_high
            lo = q.historical_low
            close = q.close
            high = q.high
            low = q.low
                  
            if (name not in traded_stocks) and close>hi:
                traded_stocks.append(name)
                
                if(name == instrument_list[0]):
                    # square_off=100
                    stop_loss = hi-50
                else:
                    # square_off=50
                    stop_loss = hi-30
                print(f"Entry {name} {high} {hi}")
                Papertrade.objects.create(start_time=datetime.datetime.now().time().strftime("%H:%M"),username=algotrade_username, signal='BUY', name=name, quantity=50,
                                        buy_price=hi+20, sell_price=hi+20, stop_loss=stop_loss,sl_trail=True,Invested=(hi+20)*50)


            if (name not in traded_stocks) and close<lo:
                print(f"Exit {name} {low} {lo}")
                traded_stocks.append(name)
                
                if(name == instrument_list[0]):
                    # square_off = 100
                    stop_loss = lo + 50
                else:
                    # square_off=50
                    stop_loss = lo + 30
                Papertrade.objects.create(start_time=datetime.datetime.now().time().strftime("%H:%M"),username=algotrade_username, signal='SELL', name=name, quantity=50 ,
                                        buy_price=lo-20, sell_price=lo-20, stop_loss=stop_loss,sl_trail=True,Invested=(lo-20)*50)
            
        interval = 60 - time.time() + start
        time.sleep(interval)
