from .serializers import StrategiesSerializer, CredentialSerializer, PapertradeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Strategies, Papertrade
from registerLogin.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import importlib
import multiprocessing
import datetime
from datetime import datetime, timedelta
from optionchain.models import LTP

process_list = {}


@api_view(['POST'])
def post_cred(request):
    data = request.data
    serializer = CredentialSerializer(data=data)
    if serializer.is_valid():

        serializer.save()
        details = CustomUser.objects.get(username=serializer.data["userName"])
        details.isCredential = True
        details.save(update_fields=['isCredential'])
        return Response({'msg': 'Credentials saved'}, status=status.HTTP_200_OK)

    return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def make_file(request, pk):
    try:
        detail = Strategies.objects.get(pk=pk)
        username = request.user
        cred = CustomUser.objects.select_related('credentials').get(username=username)

        # Write user config and algotrade_username
        file_object = open(f"strategiesAPI/user_files/{username}.py", "w")
        file_object.write("# config\n"
                          f'username = "{cred.aliceBlueID}"\npassword = "{cred.credentials.password}"\n'
                          f'app_id = "{cred.credentials.api_key}"\napi_secret = "{cred.credentials.api_secret}"\n'
                          f'twoFA = "{cred.credentials.twoFA}"\nalgotrade_username = "{username}"\n\n')
        file_object.close()

        # Append strategy to file
        script_file = open(f"{detail.filePath}", "r")
        script_data = script_file.read()
        file_object = open(f"strategiesAPI/user_files/{username}.py", "a")
        file_object.write(script_data)
        file_object.close()

        return Response({"response": "Unique File Created."}, status=status.HTTP_200_OK)

    except KeyError:
        return Response({'response": "Oops. Your have given a wrong field. "username" expected'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def execute_strategy(request):
    global process_list
    try:
        username = request.user
        file = f"strategiesAPI.user_files.{username}"
        mod = importlib.import_module(file)
        t = multiprocessing.Process(target=mod.main)
        process_list[username] = t
        print(process_list)
        t.start()
        return Response({"response": "Strategy Executed!"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'response": "Oops. Your have given a wrong field. "username" expected'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stop_strategy(request):
    global process_list
    try:
        username = request.user
        process_list[username].terminate()
        del process_list[username]
        print(process_list)
        return Response({"response": "Strategy Stopped!"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'response": "Oops. Your have given a wrong field. "username" expected'},
                        status=status.HTTP_400_BAD_REQUEST)


# noinspection PyUnusedLocal
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_strategies(request):
    queryset = Strategies.objects.all()
    serializer = StrategiesSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def execute_paper_trade(request):
    global process_list
    try:
        username = request.user
        file = f"strategiesAPI.user_files.{username}"
        mod = importlib.import_module(file)
        t = multiprocessing.Process(target=mod.start_paper_trade)
        process_list[username] = t
        print(process_list)
        t.start()
        return Response({"response": "PaperTrade Executed!"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'response": "Oops. Your have given a wrong field. "username" expected'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_paper_trades(request):
    try:
        username = request.user
        start_date = datetime.today()
        end_date = datetime.today()
        queryset = Papertrade.objects.all().filter(username=username).filter(
            date__range=[start_date, end_date])
        for item in queryset.iterator():
            if item.isCompleted == False:
                name = item.get_name()
                item.ltp = LTP.objects.get(name=name).ltp
            item.set_active()
            item.sl_trailing()
            item.set_complete(username)
            item.set_npl()
            item.save()
        serializer = PapertradeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except KeyError:
        return Response(
            {
                'response": "Oops. Your have given a wrong field. "username" expected'
            },
            status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_name(request):
    try:
        username = request.user
        name = request.data['name']
    
        q = Papertrade.objects.all().filter(username=username).filter(isActive = True).filter(isCompleted = False).get(name = name)
        q.manual_stop(username)
        q.set_npl()
        q.save()
       
        return Response({"response":"Square Off Successful"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response(
            {
                'response": "Oops. Your have given a wrong field. "username" expected'
            },
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    try:
        username = request.user
        delta = request.data['delta']
        if delta == -1:
            queryset = Papertrade.objects.all().filter(username=username).filter(
                isCompleted=True)

        else:
            start_date = datetime.today() - timedelta(days=delta)
            end_date = datetime.today()
            queryset = Papertrade.objects.all().filter(username=username).filter(
                isCompleted=True).filter(date__range=[start_date, end_date])
        serializer = PapertradeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except KeyError:
        return Response(
            {
                'response": "Oops. Your have given a wrong field. "username" expected'
            },
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stop_paper_trades(request):
    try:
        username = request.user
        process_list[username].terminate()
        del process_list[username]
        print(process_list)
        return Response({"response": "Fields Deleted!"}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({'response": "Oops. Your have given a wrong field. "username" expected'},
                        status=status.HTTP_400_BAD_REQUEST)
 