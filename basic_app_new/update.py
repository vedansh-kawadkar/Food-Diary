from django import forms
from basic_app_new.models import *

class UpdateFood(forms.ModelForm):
    class Meta:
        model = Old_Food_Diary
        fields = ['mfg_code', 'food_name', 'description', 'food_type', 'calories', 'fats', 'protein', 'carbohydrates', 'link_of_image', 'link_of_recipie', 'purchasing_link']

class UpdatePurchaseFood(forms.ModelForm):
    class Meta:
        model = purchase_cards
        fields = ['food_name', 'description', 'ss_code', 'calorie', 'fat', 'protein', 'carbs', 'image_path']