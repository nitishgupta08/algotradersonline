import datetime
import time
import threading
import pandas as pd
import json
import sys
import os
import django
from config import Credentials
from alice_blue import *

# To make django-models work outside django
sys.path.append("/Users/nitishgupta/Desktop/algotradersonline/backend/src")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from optionchain.models import LTP
from strategiesAPI.models import FiveMIN

df = pd.DataFrame()
df_final = pd.DataFrame()
ORB_timeFrame = 60  # in seconds


def login():
    session_id = AliceBlue.login_and_get_sessionID(
        username=Credentials.UserName.value,
        password=Credentials.PassWord.value,
        twoFA=Credentials.TwoFA.value,
        api_secret=Credentials.SecretKey.value,
        app_id=Credentials.AppId.value)
    alice = AliceBlue(username=Credentials.UserName.value,
                      session_id=session_id)

    return alice


def subscribe(alice):
    alice.start_websocket(subscribe_callback=event_handler_quote_update)

    alice.subscribe([
        alice.get_instrument_by_symbol('NSE', i.upper() + '-EQ') for i in SCRIPT_LIST
    ], LiveFeedType.TICK_DATA)


def event_handler_quote_update(message):
    global df

    ltp = message['ltp']
    instrument = message['instrument'].symbol

    p, created = LTP.objects.get_or_create(name=instrument)
    p.ltp = ltp
    p.save()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    exchange = message['instrument'].exchange
    # atp = message['atp']
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
        q, created = FiveMIN.objects.get_or_create(name=name)
        q.timestamp = timestamp
        q.volume = volume
        q.open = open
        q.close = close
        q.high = high
        q.low = low
        q.exchange = exchange
        # q.atp = atp
        q.save()


if __name__ == '__main__':
    with open('script_list.txt', 'r') as filehandle:
        SCRIPT_LIST = json.loads(filehandle.read())

    # while ((datetime.datetime.now().time() <= datetime.time(9, 14, 00))
    #        or (datetime.datetime.now().time() >= datetime.time(22, 30, 00))):
    #     pass

    alice_obj = login()
    subscribe(alice_obj)

    main_interval = (5 - datetime.datetime.now().minute % 5) * 60 - (
        datetime.datetime.now().second)
    print("start in ", main_interval)
    time.sleep(main_interval)
    create_ohlc()
