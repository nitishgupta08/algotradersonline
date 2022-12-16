from django.contrib import admin
from .models import LTP, NIFTY, NIFTY_histo, BANKNIFTY_histo, BANKNIFTY
# Register your models here.


@admin.register(LTP)
class LTPAdmin(admin.ModelAdmin):
    list_display = ['name', 'ltp']
    search_fields = ("name__startswith", )


@admin.register(NIFTY)
class NIFTYAdmin(admin.ModelAdmin):
    list_display = ['Strike_Price', 'OI_C', 'LTP_C', 'LTP_P', 'OI_P']
    search_fields = ("Strike_Price__startswith", )


@admin.register(NIFTY_histo)
class NIFTYHistoAdmin(admin.ModelAdmin):
    list_display = ['date_time', 'Strike_Price', 'OI_C', 'LTP_C', 'LTP_P', 'OI_P']
    search_fields = ("date_time__startswith", )


@admin.register(BANKNIFTY)
class BANKNIFTYAdmin(admin.ModelAdmin):
    list_display = ['Strike_Price', 'OI_C', 'LTP_C', 'LTP_P', 'OI_P']
    search_fields = ("Strike_Price__startswith", )


@admin.register(BANKNIFTY_histo)
class BANKNIFTYHistoAdmin(admin.ModelAdmin):
    list_display = ['date_time', 'Strike_Price', 'OI_C', 'LTP_C', 'LTP_P', 'OI_P']
    search_fields = ("date_time__startswith", )