from django.db import models
from django.conf import settings
import os
from registerLogin.models import CustomUser
import datetime
import hashlib


def scripts_path():
    return os.path.join(settings.BASE_DIR, 'strategiesAPI/scripts')


class Strategies(models.Model):
    name = models.CharField(max_length=20)
    filePath = models.FilePathField(path=scripts_path(), unique=True)
    isProduction = models.BooleanField(default=False,verbose_name='Production')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Strategie"


class Credentials(models.Model):
    userName = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    twoFA = models.CharField(max_length=4)
    password = models.CharField(max_length=50)
    api_key = models.CharField(max_length=100)
    api_secret = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.userName}"

    class Meta:
        verbose_name = "Credential"


class Papertrade(models.Model):
    username = models.CharField(max_length=100)
    signal = models.CharField(max_length=50)
    name = models.CharField(max_length=50, verbose_name='Stock Name')
    quantity = models.IntegerField()
    buy_price = models.FloatField()
    sell_price = models.FloatField()
    stop_loss = models.FloatField(default=0.0)
    target = models.FloatField(default=100000)
    isCompleted = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)
    start_time = models.CharField(max_length=100,
                                  default="00:00",
                                  verbose_name='Trade Started at')
    end_time = models.CharField(max_length=100,
                                default="00:00",
                                verbose_name='Trade Ended at')
    date = models.DateField(default=datetime.datetime.now, blank=True)
    historical_volume = models.IntegerField(default=0,verbose_name='Historical Volume')
    current_volume = models.IntegerField(default=0,verbose_name='Current Volume')
    ltp = models.FloatField(default=0.0, verbose_name='LTP')
    net_pl = models.FloatField(default=0.0, verbose_name='Net P/L')
    net_charges = models.FloatField(default=0.0,  verbose_name='Total Charges')
    sl_trail=models.BooleanField(default=False)
    Invested=models.FloatField(default=100000)
    
    def set_active(self):
        if (self.signal == "BUY" and self.ltp >= self.buy_price
            and self.isActive == False and self.ltp !=0) or (self.signal == "SELL"
                                            and self.sell_price >= self.ltp
                                            and self.isActive == False and self.ltp!=0):
            self.isActive = True

    def set_complete(self, username):
        if self.isActive is True and self.isCompleted is False:
            if self.signal == "BUY":
                if (self.ltp >= (self.buy_price + self.target) or self.ltp <=
                        self.stop_loss):
                    self.isCompleted = True
                    self.sell_price = self.ltp
                    self.end_time=datetime.datetime.now().time().strftime("%H:%M")
                    TradedStocks.objects.all().filter(
                        username=username).filter(
                        stock_name=self.name).delete()
            elif self.signal == "SELL":
                if (self.ltp <= (self.sell_price - self.target) or self.ltp >=
                        self.stop_loss):
                    self.isCompleted = True
                    self.buy_price = self.ltp
                    self.end_time=datetime.datetime.now().time().strftime("%H:%M")
                    TradedStocks.objects.all().filter(
                        username=username).filter(
                        stock_name=self.name).delete()

    def sl_trailing(self):
        if self.isActive is True and self.isCompleted is False and self.sl_trail is True:
            if self.signal == "BUY":
                if (self.ltp-self.sell_price>=30):
                    self.sell_price = self.ltp
                    self.stop_loss+=30
            elif self.signal == "SELL":
                if (self.buy_price-self.ltp>=30):
                    self.buy_price = self.ltp
                    self.stop_loss-=30
    
    def manual_stop(self,username):
        if self.isActive is True and self.isCompleted is False:
            if self.signal == "BUY":
                self.isCompleted = True
                self.sell_price = self.ltp
                self.end_time=datetime.datetime.now().time().strftime("%H:%M")
                TradedStocks.objects.all().filter(
                    username=username).filter(
                    stock_name=self.name).delete()
            elif self.signal == "SELL":
                self.isCompleted = True
                self.buy_price = self.ltp
                self.end_time=datetime.datetime.now().time().strftime("%H:%M")
                TradedStocks.objects.all().filter(
                    username=username).filter(
                    stock_name=self.name).delete()


    def set_npl(self):
        if (self.isActive is True and self.isCompleted is True
                and self.net_charges == 0.0):
            turnover = (self.buy_price + self.sell_price) * self.quantity
            stt = self.sell_price * self.quantity * 0.00025
            brokerage = min(turnover * 0.0001, 40)
            tran_charges = turnover * 0.0000325
            sebi_charges = turnover * 0.000002
            stamp_duty = turnover * 0.0001
            service_tax = (brokerage + tran_charges) * 0.15
            self.net_charges = brokerage + tran_charges + sebi_charges + stamp_duty + service_tax + stt
            self.net_pl = (self.sell_price - self.buy_price) * self.quantity - self.net_charges
        elif (self.isActive is True and self.isCompleted is True
                and self.net_charges == 200 and self.net_pl==0.0):
            self.net_pl = (self.sell_price - self.buy_price) * self.quantity - self.net_charges
                
    def __str__(self):
        return f"{self.username} {self.name}"

    def get_name(self):
        return self.name


class TradedStocks(models.Model):
    username = models.CharField(max_length=100)
    stock_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} {self.stock_name}"

    class Meta:
        verbose_name = "Traded Stock"


class OneMIN(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)
    volume = models.IntegerField(default=0)
    open = models.FloatField(default=0)
    close = models.FloatField(default=0)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    atp = models.FloatField(default=0)
    exchange = models.CharField(max_length=20)
    historical_volume = models.IntegerField(default=0)
    historical_high = models.FloatField(default=0)
    historical_low = models.FloatField(default=0)
    
    class Meta:
        verbose_name = "1 MIN Candle Data"


class FiveMIN(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)
    volume = models.IntegerField(default=0)
    open = models.FloatField(default=0)
    close = models.FloatField(default=0)
    high = models.FloatField(default=0)
    low = models.FloatField(default=0)
    atp = models.FloatField(default=0)
    exchange = models.CharField(max_length=20)
    historical_volume = models.IntegerField(default=0)

    class Meta:
        verbose_name = "5 MIN Candle Data"
