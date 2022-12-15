from django.contrib import admin
from .models import Strategies, Credentials, Papertrade, TradedStocks, OneMIN, FiveMIN


# Register your models here.


@admin.register(Strategies)
class StrategiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'isProduction')


@admin.register(Credentials)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ['userName']


@admin.register(Papertrade)
class PaperTradeAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'isActive', 'isCompleted', 'date']
    search_fields = ("username__startswith", )
    fields = [
        'username', ('signal', 'name'),
        ('quantity', 'buy_price', 'sell_price'), ('stop_loss', 'target'),
        ('isActive', 'isCompleted'), ('start_time', 'end_time', 'date'), ("historical_volume", "current_volume"), 'ltp',
        ('net_pl', 'net_charges','Invested')
    ]
    list_filter = ("username", "date" )


@admin.register(TradedStocks)
class TradedStocksAdmin(admin.ModelAdmin):
    list_display = ['username', 'stock_name']
    

@admin.register(OneMIN)
class OneMinAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'name', 'exchange', 'volume']
    search_fields = ("name__startswith",)
    list_filter = ("exchange",)


@admin.register(FiveMIN)
class FiveMinAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'name', 'exchange', 'volume']
    search_fields = ("name__startswith",)
    list_filter = ("exchange",)
