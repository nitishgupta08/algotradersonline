from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import LTP, NIFTY, NIFTY_histo, BANKNIFTY_histo, BANKNIFTY
from .serializers import LTPSerializer, NIFTYSerializer, NIFTYHistoSerializer, BANKNIFTYSerializer, BANKNIFTYHistoSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_banknifty(request):
    queryset = BANKNIFTY.objects.all()
    serializer = BANKNIFTYSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_banknifty_histo(request):
    date = request.data["date"]
    date = datetime.fromisoformat(date[:-1]+"+00:00").replace(second=0, microsecond=0)
    queryset = BANKNIFTY_histo.objects.all().filter(date_time=date)
    serializer = BANKNIFTYHistoSerializer(queryset, many=True)
    print(date)
    return Response(serializer.data, status=status.HTTP_200_OK)