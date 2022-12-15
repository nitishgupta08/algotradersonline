from django.db import models


class LTP(models.Model):
    name = models.CharField(max_length=100)
    ltp = models.FloatField(default=0.0)
    chn_prev_day = models.FloatField(default=0.0)
    per_chn = models.FloatField(default=0.0)
    oi_per_chn = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} {self.ltp}"


class NIFTY(models.Model):
    Volume_C = models.FloatField(default=0.0)
    OI_Change_C = models.FloatField(default=0.0)
    OI_C = models.FloatField(default=0.0)
    LTP_C = models.FloatField(default=0.0)
    Strike_Price = models.FloatField(primary_key=True, verbose_name='Strike Price')
    LTP_P = models.FloatField(default=0.0)
    OI_P = models.FloatField(default=0.0)
    OI_Change_P = models.FloatField(default=0.0)
    Volume_P = models.FloatField(default=0.0)
    PUT_CALL_OI_CHN = models.FloatField(verbose_name='PUT-CALL OI CHN', default=0.0)
    PUT_CALL_OI = models.FloatField(verbose_name='PUT-CALL OI', default=0.0)
    PCR = models.FloatField(verbose_name='PCR (Bullish)', default=0.0)
    CPR = models.FloatField(verbose_name='CPR (Bearish)', default=0.0)
    STRONGNESS_OF_SUPPORT = models.FloatField(default=0.0)
    Reverse_Weightage = models.FloatField(default=0.0)
    Buy_Sell = models.CharField(max_length=100, verbose_name='Buy/Sell', default="-")
    Stongness_Level = models.CharField(max_length=100, default="-")
    Immediate_Support = models.FloatField(default=0.0)
    Strong_Support = models.FloatField(default=0.0)
    PCR_Weightage = models.FloatField(default=0.0)
    CPR_Weightage = models.FloatField(default=0.0)

    def __str__(self):
        return f"NIFTY {self.Strike_Price}"


class NIFTY_histo(models.Model):
    date_time = models.DateTimeField()
    Volume_C = models.FloatField(default=0.0)
    OI_Change_C = models.FloatField(default=0.0)
    OI_C = models.FloatField(default=0.0)
    LTP_C = models.FloatField(default=0.0)
    Strike_Price = models.FloatField(verbose_name='Strike Price')
    LTP_P = models.FloatField(default=0.0)
    OI_P = models.FloatField(default=0.0)
    OI_Change_P = models.FloatField(default=0.0)
    Volume_P = models.FloatField(default=0.0)
    PUT_CALL_OI_CHN = models.FloatField(verbose_name='PUT-CALL OI CHN', default=0.0)
    PUT_CALL_OI = models.FloatField(verbose_name='PUT-CALL OI', default=0.0)
    PCR = models.FloatField(verbose_name='PCR (Bullish)', default=0.0)
    CPR = models.FloatField(verbose_name='CPR (Bearish)', default=0.0)
    STRONGNESS_OF_SUPPORT = models.FloatField(default=0.0)
    Reverse_Weightage = models.FloatField(default=0.0)
    Buy_Sell = models.CharField(max_length=100, verbose_name='Buy/Sell', default="-")
    Stongness_Level = models.CharField(max_length=100, default="-")
    Immediate_Support = models.FloatField(default=0.0)
    Strong_Support = models.FloatField(default=0.0)
    PCR_Weightage = models.FloatField(default=0.0)
    CPR_Weightage = models.FloatField(default=0.0)

    def __str__(self):
        return f"NIFTY {self.Strike_Price}"