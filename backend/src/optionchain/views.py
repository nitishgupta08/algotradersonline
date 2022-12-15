from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import LTP, NIFTY, NIFTY_histo
from .serializers import LTPSerializer, NIFTYSerializer, NIFTYHistoSerializer
from rest_framework.permissions import IsAuthenticated
import requests
import json
from datetime import datetime
from pytz import timezone

indexes = ["BANKNIFTY", "NIFTY"]
url_oc = "https://www.nseindia.com/option-chain"
url_bnf = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
url_nf = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
url_indices = "https://www.nseindia.com/api/allIndices"

headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
        'Safari/537.36',
    'accept-language': 'en,gu;q=0.9,hi;q=0.8',
    'accept-encoding': 'gzip, deflate, br'
}

sess = requests.Session()
cookies = dict()


def set_cookie():
    global cookies
    request = sess.get(url_oc, headers=headers, timeout=5)
    cookies = dict(request.cookies)


def get_data(url):
    set_cookie()
    response = sess.get(url, headers=headers, timeout=5, cookies=cookies)

    if response.status_code == 401:
        set_cookie()
        response = sess.get(url_nf,
                            headers=headers,
                            timeout=5,
                            cookies=cookies)
    if response.status_code == 200:
        return response.text
    return ""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def option_data(request):
    date = request.data["date"]
    symbol = request.data["symbol"]
    if symbol in indexes:
        if symbol == 'BANKNIFTY':
            ltp = LTP.objects.all().get(name='Nifty Bank')
        else:
            ltp = LTP.objects.all().get(name='Nifty 50')
        options = json.loads(get_data("https://www.nseindia.com/api/option-chain-indices?symbol=" + symbol))["records"]
    else:
        options = json.loads(get_data("https://www.nseindia.com/api/option-chain-equities?symbol=" + symbol))["records"]
        ltp = LTP.objects.all().get(name=symbol)

    expiry_dates = options["expiryDates"]
    serializer = LTPSerializer(ltp)

    if date == "":
        data = [d for d in options["data"] if d["expiryDate"] == expiry_dates[0]]
    else:
        data = [d for d in options["data"] if d["expiryDate"] == date]

    return Response([data, expiry_dates, [serializer.data]], status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_ltp(request):
    try:
        instrument = request.data['instrument']
        queryset = LTP.objects.none()
        for i in instrument:
            queryset |= LTP.objects.all().filter(name=i)
        serializer = LTPSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'response: Provided Instrument does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nifty(request):
    queryset = NIFTY.objects.all()
    serializer = NIFTYSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_nifty_histo(request):
    date = request.data["date"]
    date = datetime.fromisoformat(date[:-1]+"+00:00").replace(second=0, microsecond=0)
    queryset = NIFTY_histo.objects.all().filter(date_time=date)
    serializer = NIFTYHistoSerializer(queryset, many=True)
    print(date)
    return Response(serializer.data, status=status.HTTP_200_OK)