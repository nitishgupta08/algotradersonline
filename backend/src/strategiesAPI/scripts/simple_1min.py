import time
from alice_blue import *
import dateutil.parser
import datetime
import pandas as pd
import pandasql as ps
import requests
import django
django.setup()
from ..models import Papertrade, TradedStocks, OneMIN

traded_stocks = []
instrument_list = [
    'ACC', 'ADANIENT', 'ADANIPORTS', 'AMBUJACEM', 'APOLLOHOSP', 'ASIANPAINT', 'AUBANK',
    'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BATAINDIA', 'BHARATFORG',
    'BHARTIARTL', 'BIOCON', 'BPCL', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COFORGE', 'DABUR',
    'DIVISLAB', 'DLF', 'DRREDDY', 'EICHERMOT', 'GODREJCP', 'GODREJPROP', 'GRASIM', 'HAVELLS',
    'HCLTECH', 'HDFC', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO', 'HINDPETRO',
    'HINDUNILVR', 'ICICIBANK', 'ICICIPRULI', 'IGL', 'INDIGO', 'INDUSINDBK', 'INFY',
    'IRCTC', 'ITC', 'JINDALSTEL', 'JSWSTEEL', 'JUBLFOOD', 'KOTAKBANK', 'LICHSGFIN',
    'LT', 'LTI', 'LUPIN', 'M&M', 'MARUTI', 'MINDTREE', 'MUTHOOTFIN',
    'PEL', 'PIDILITIND', 'PVR', 'RELIANCE', 'SBICARD', 'SBILIFE', 'SBIN', 'SRF',
    'SRTRANSFIN', 'SUNPHARMA', 'TATACHEM', 'TATACONSUM', 'TATAMOTORS', 'TATAPOWER',
    'TATASTEEL', 'TCS', 'TECHM', 'TITAN', 'TVSMOTOR', 'UPL', 'VEDL', 'VOLTAS', 'WIPRO',
    'ZEEL'
]

session_id = AliceBlue.login_and_get_sessionID(username=username,
                                                    password=password,
                                                    twoFA=twoFA,
                                                    api_secret=api_secret,
                                                    app_id=app_id)
alice = AliceBlue(username=username,
                      session_id=session_id)


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
    instrument = alice.get_instrument_by_symbol("NSE", i)
    date = datetime.datetime.strptime('2017-05-04', "%Y-%m-%d")
    date_start = date.replace(minute=15,
                              hour=9,
                              second=00,
                              year=datetime.datetime.now().year,
                              month=datetime.datetime.now().month,
                              day=datetime.datetime.now().day)
    date_end = date.replace(minute=30,
                            hour=15,
                            second=00,
                            year=datetime.datetime.now().year,
                            month=datetime.datetime.now().month,
                            day=datetime.datetime.now().day)
    if datetime.datetime.now().weekday() == 0:
        from_datetime = date_start - datetime.timedelta(
            days=3)
        to_datetime = date_end - datetime.timedelta(
            days=3)
    else:
        from_datetime = date_start - datetime.timedelta(
            days=1)
        to_datetime = date_end - datetime.timedelta(
            days=1)
    interval1 = "1_MIN"  # ["DAY", "1_HR", "3_HR", "1_MIN", "5_MIN", "15_MIN", "60_MIN"]
    indices = False
    df1 = pd.DataFrame(
        get_historical(instrument, from_datetime, to_datetime, interval1,
                       indices))

    q1 = """SELECT  volume FROM df1 order by volume DESC LIMIT 1 """
    s1 = ps.sqldf(q1, locals())
    vol = s1["volume"][0]

    return vol


def main():
    for name in instrument_list:
        vo = test(name)
        q = OneMIN.objects.all().get(name=name)
        q.historical_volume = vo
        q.save()
        print(f"{name}: {vo}")

    while datetime.datetime.now().time() < datetime.time(9, 15, 00):
        pass
   
    interval = 60 - datetime.datetime.now().second
    time.sleep(interval + 2)

    while datetime.time(9, 16, 2) <= datetime.datetime.now().time() <= datetime.time(15, 25, 5):
        start = time.time()
        print(f'1MIN candle at {datetime.datetime.now().time().strftime("%H:%M")}')
       
        for name in instrument_list:
            q = OneMIN.objects.get(name=name)
            vo = q.historical_volume
            vol = q.volume
            open = q.open
            close = q.close
            high = q.high
            low = q.low
            # atp = q.atp
            range_oc2 = close - open
            range_hl2 = high - low
            range_hl1 = high - low
            range_oc1 = open - close
            money = 100000
            l1 = low - low * 0.1 / 100
            h1 = high + high * 0.1 / 100

            if (name not in traded_stocks) and (vol > vo) and (open < close) and (range_oc2 > range_hl2 * 0.80):
                traded_stocks.append(name)
                print(f"Entry {name} {vol} {vo}")
                alice.place_order(transaction_type=TransactionType.Buy,
                                  instrument=alice.get_instrument_by_symbol(
                                      'NSE', name),
                                  quantity=1,
                                  order_type=OrderType.StopLossLimit,
                                  product_type=ProductType.BracketOrder,
                                  price=float(high),
                                  trigger_price=float(high),
                                  stop_loss=3.0,
                                  square_off=5.0,
                                  trailing_sl=20,
                                  is_amo=None)

            if (name not in traded_stocks) and (vol > vo) and (open > close) and (range_oc1 > range_hl1 * 0.80):
                print(f"Exit {name} {vol} {vo}")
                traded_stocks.append(name)
                alice.place_order(transaction_type=TransactionType.Sell,
                                  instrument=alice.get_instrument_by_symbol(
                                      'NSE', name),
                                  quantity=1,
                                  order_type=OrderType.StopLossLimit,
                                  product_type=ProductType.BracketOrder,
                                  price=float(low),
                                  trigger_price=float(low),
                                  stop_loss=3.0,
                                  square_off=5.0,
                                  trailing_sl=20,
                                  is_amo=None)
           
        interval = 60 - (time.time() - start)
        time.sleep(interval)


def start_paper_trade():
    # noinspection PyGlobalUndefined
    global algotrade_username
    for name in instrument_list:
        vo = test(name)
        q = OneMIN.objects.get(name=name)
        q.historical_volume = vo
        q.save()
        print(f"{name}: {vo}")

    while datetime.datetime.now().time() < datetime.time(9, 15, 00):
        pass
 
    interval = 60 - datetime.datetime.now().second
    time.sleep(interval + 2)

    while datetime.time(9, 16, 0) <= datetime.datetime.now().time() <= datetime.time(15,0,0):
        start = time.time()
        print(f'1MIN candle at {datetime.datetime.now().time().strftime("%H:%M")}')
        
        for name in instrument_list:
            q = OneMIN.objects.get(name=name)
            vo = q.historical_volume
            vol = q.volume
            open = q.open
            close = q.close
            high = q.high
            low = q.low
            # atp = q.atp
            range_oc2 = close - open
            range_hl2 = high - low
            range_hl1 = high - low
            range_oc1 = open - close
            money = 100000
            l1 = low - low * 0.1 / 100
            h1 = high + high * 0.1 / 100
            quantity_b = int(money / h1)
            quantity_s = int(money / l1)
           
            if ((not TradedStocks.objects.filter(username=algotrade_username).filter(stock_name=name).exists()) and (vol > vo) and (open < close)
                    and (range_oc2 > range_hl2 * 0.90)):
                stop_loss = high+0.5- (high-low)/2
                square_off = (high - low)
                print(f"Entry {name} {vol} {vo}")
                TradedStocks.objects.create(username=algotrade_username,stock_name=name)
                
                Papertrade.objects.create(start_time=datetime.datetime.now().time().strftime("%H:%M"),username=algotrade_username, signal='BUY', name=name, quantity=quantity_b,
                                          buy_price=high+0.5, sell_price=0, stop_loss=stop_loss, target=square_off,historical_volume=vo,current_volume=vol)
                
                Papertrade.objects.create(start_time=datetime.datetime.now().time().strftime("%H:%M"),username=algotrade_username, signal='SELL', name=name, quantity=quantity_b,
                                          buy_price=0, sell_price=stop_loss, stop_loss=high+0.5, target=square_off,historical_volume=vo,current_volume=vol)

            if ((not TradedStocks.objects.filter(username=algotrade_username).filter(stock_name=name).exists()) and (vol > vo) and (open > close) and (range_oc1 > range_hl1 * 0.90)):
                print(f"Exit {name} {vol} {vo}")
         
                stop_loss = low-0.5+ (high-low)/2
                square_off = (high - low)
                TradedStocks.objects.create(username=algotrade_username,stock_name=name)

                Papertrade.objects.create(start_time=datetime.datetime.now().time().strftime("%H:%M"),username=algotrade_username, signal='SELL', name=name, quantity=quantity_s,
                                          buy_price=0, sell_price=low-0.5, stop_loss=stop_loss, target=square_off,historical_volume=vo,current_volume=vol)
                
                Papertrade.objects.create(start_time=datetime.datetime.now().time().strftime("%H:%M"),username=algotrade_username, signal='BUY', name=name, quantity=quantity_s,
                                          buy_price=stop_loss, sell_price=0, stop_loss=low-0.5, target=square_off,historical_volume=vo,current_volume=vol)

        interval = 60 - time.time() + start
        time.sleep(interval)
