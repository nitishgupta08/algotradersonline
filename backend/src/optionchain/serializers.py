from rest_framework import serializers
from .models import LTP, NIFTY, NIFTY_histo


class LTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = LTP
        fields = '__all__'


class NIFTYSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIFTY
        fields = '__all__'

class NIFTYHistoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIFTY_histo
        fields = '__all__'
