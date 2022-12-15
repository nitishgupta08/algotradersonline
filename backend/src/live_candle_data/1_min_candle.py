import datetime
import time
import threading
from alice_blue import *
import pandas as pd
from config import Credentials
# To make django-models work outside django
import sys
import os
import django

sys.path.append("/Users/nitishgupta/Desktop/algotradersonline/backend/src")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from optionchain.models import LTP
from strategiesAPI.models import OneMIN

SCRIPT_LIST = [
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
    'ZEEL']

socket_opened = False
df = pd.DataFrame()
df_final = pd.DataFrame()
ORB_timeFrame = 60  # in seconds
x = 1

bank = ""
nifty = ""


def login():
    global bank
    global nifty
    session_id = AliceBlue.login_and_get_sessionID(
        username=Credentials.UserName.value,
        password=Credentials.PassWord.value,
        twoFA=Credentials.TwoFA.value,
        api_secret=Credentials.SecretKey.value,
        app_id=Credentials.AppId.value)
    alice = AliceBlue(username=Credentials.UserName.value,
                      session_id=session_id)

    # alice.start_websocket(subscribe_callback=event_handler_quote_update)
    # alice.subscribe([
    #     alice.get_instrument_by_symbol('NSE', i.upper() + '-EQ') for i in SCRIPT_LIST
    # ], LiveFeedType.TICK_DATA)
    #
    # alice.subscribe(alice.get_instrument_by_symbol('NSE', 'NIFTY 50'),
    #                 LiveFeedType.TICK_DATA)
    #
    # alice.subscribe(alice.get_instrument_by_symbol('NSE', 'NIFTY BANK'),
    #                 LiveFeedType.TICK_DATA)
    # alice.subscribe(alice.get_instrument_by_symbol('NSE', 'INDIA VIX'),
    #                 LiveFeedType.TICK_DATA)
    # print(alice.search_instruments('NFO', 'NIFTY'))

    # Get monthly and weekly expiry
    df = pd.DataFrame(alice.search_instruments('NFO', 'BANKNIFTY'))
    df = df.filter(['expiry'])  # Filter only expiry dates
    df.drop_duplicates(inplace=True)  # keeping unique values
    df = df.sort_values(by=['expiry'], ascending=True)
    arr = df.to_numpy()  # Converts it to a 2D array of size n x 1
    t = arr[0][0].month  # Getting the month of the first date
    for i in range(0, len(arr)):
        if arr[i][0].month > t:
            break
        date = arr[i][0]  # This will save the monthly expiry

    print(alice.get_instrument_for_fno(symbol = 'NIFTY2320218150PE'))
    # q = LTP.objects.get(name='Nifty Bank')
    # x = q.ltp
    # x = (int)(x / 100) * 100
    # for i in range(x - 1000, x + 1000, 100):
    #     alice.subscribe(alice.get_instrument_for_fno(symbol='BANKNIFTY',
    #                                                  expiry_date=arr[0][0],
    #                                                  is_fut=False,
    #                                                  strike=i,
    #                                                  is_CE=False),
    #                     LiveFeedType.TICK_DATA)
    #     alice.subscribe(alice.get_instrument_for_fno(symbol='BANKNIFTY',
    #                                                  expiry_date=arr[0][0],
    #                                                  is_fut=False,
    #                                                  strike=i,
    #                                                  is_CE=True),
    #                     LiveFeedType.TICK_DATA)
    #
    # q = LTP.objects.get(name='Nifty 50')
    # y = q.ltp
    # y = (int)(y / 100) * 100
    # for i in range(y - 1000, y + 1000, 100):
    #     alice.subscribe(alice.get_instrument_for_fno(symbol='NIFTY',
    #                                                  expiry_date=arr[0][0],
    #                                                  is_fut=False,
    #                                                  strike=i,
    #                                                  is_CE=False),
    #                     LiveFeedType.TICK_DATA)
    #     alice.subscribe(alice.get_instrument_for_fno(symbol='NIFTY',
    #                                                  expiry_date=arr[0][0],
    #                                                  is_fut=False,
    #                                                  strike=i,
    #                                                  is_CE=True),
    #                     LiveFeedType.TICK_DATA)


def event_handler_quote_update(message):
    global df
    global bank
    global nifty
    print(message)

    ltp = message['ltp']

    token = message['instrument'].token
    if token == 26000:
        instrument = "Nifty 50"
    elif token == 26009:
        instrument = "Nifty Bank"
    else:
        instrument = message['instrument'].symbol

    p, created = LTP.objects.get_or_create(name=instrument)
    p.ltp = ltp
    p.save()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    exchange = message['instrument'].exchange

    if 'volume' in message:
        df_new = pd.DataFrame(
            {
                'symbol': instrument,
                'timestamp': timestamp,
                'ltp': ltp,
                'exchange': exchange,
                'volume': message['volume']
            },
            index=[0])
        df = pd.concat([df, df_new], ignore_index=True)


def create_ohlc():
    start = time.time()
    global df
    copydf = df.copy(deep=True).drop_duplicates()
    df = df.iloc[0:0]
    get_ohlc(copydf)
    interval = ORB_timeFrame - (time.time() - start)
    print(
        f"Next check will start after {interval} sec : {datetime.datetime.now()}"
    )

    threading.Timer(interval, create_ohlc).start()


def get_ohlc(dataframe):
    grouped = dataframe.groupby('symbol')

    global df_final
    global x
    # book = load_workbook(
    #     f'/home/vmadmin/Desktop/backend/day_data/{datetime.datetime.now().strftime("%Y-%m-%d")}_1MIN.xlsx')
    # writer = pd.ExcelWriter(
    #     f'/home/vmadmin/Desktop/backend/day_data/{datetime.datetime.now().strftime("%Y-%m-%d")}_1MIN.xlsx',
    #     engine='openpyxl')
    # writer.book = book
    # writer.sheets = {ws.title: ws for ws in book.worksheets}

    for name, group in grouped:
        group = group.sort_values('timestamp')
        timestamp = group['timestamp'].iloc[0]
        symbol = name
        volume = group['volume'].iloc[-1] - group['volume'].iloc[0]
        open = group['ltp'].iloc[0]
        close = group['ltp'].iloc[-1]
        high = group['ltp'].max()
        low = group['ltp'].min()
        exchange = group['exchange'].iloc[0]
        # atp = group['atp'].iloc[-1]
        q, created = OneMIN.objects.get_or_create(name=name)
        q.timestamp = timestamp
        q.volume = volume
        q.open = open
        q.close = close
        q.high = high
        q.low = low
        q.exchange = exchange
        # q.atp = atp
        q.save()
        data = {
            'timestamp': timestamp,
            'symbol': symbol,
            'volume': volume,
            'open': open,
            'close': close,
            'high': high,
            'low': low,
            'exchange': exchange,
            # 'atp':atp
        }

        df_append = pd.DataFrame(data, index=[0])
        # df_append.to_excel(writer, header=False, index=False, startrow=x, startcol=0)
        x += 1
    # writer.save()
    # book.close()


if __name__ == '__main__':
    # while ((datetime.datetime.now().time() <= datetime.time(9, 14, 00))
    #        or (datetime.datetime.now().time() >= datetime.time(22, 30, 00))):
    #     pass

    login()
    main_interval = ORB_timeFrame - datetime.datetime.now().second

    print("start in ", main_interval)
    time.sleep(main_interval)
    create_ohlc()
