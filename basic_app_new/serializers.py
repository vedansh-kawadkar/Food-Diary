
from rest_framework import serializers
from basic_app_new.models import *


class Purchase_cards_serializer(serializers.ModelSerializer):
    class Meta:
        model=purchase_cards
        fields='__all__'

class Cuisine_food_items_serializer(serializers.ModelSerializer):
    class Meta:
        model=Old_Food_Diary
        fields='__all__'

class Purchase_transactions_serializer(serializers.ModelSerializer):
    class Meta:
        model=Purchase_det_new
        fields='__all__'

class Purchase_fooditem_serializer(serializers.ModelSerializer):
    class Meta:
        model=purchase_cards
        fields='__all__'
class Cuisine_fooditem_serializer(serializers.ModelSerializer):
    class Meta:
        model=Old_Food_Diary
        fields='__all__'

class Cuisine_transactions_serializer(serializers.ModelSerializer):
    class Meta:
        model=cuisine_consumption_det
        fields='__all__'
