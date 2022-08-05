from rest_framework import serializers
from .models import Ticker


class TickerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticker
        fields = [
            'id',
            'yticker',
            'date',
            'px_last',
            'px_high',
            'px_low',
            'px_open',
            'px_volume'
        ]
