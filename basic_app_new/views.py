from django.shortcuts import render, HttpResponse
from basic_app_new.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.http import JsonResponse
import requests
import json
import re
import pandas as pd
from urllib.request import urlopen
import urllib.request as urllib2
from bs4 import BeautifulSoup
from django.db.models import Q
from datetime import datetime,time,date,timedelta
from django.db.models import Q
from rest_framework.views import APIView
from basic_app_new.serializers import *
from rest_framework.response import Response

from PIL import Image
import random
total_count = Food_diary_new.objects.all().count()
print(total_count)
# Create your views here.
url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
headers = {
    "Content-Type": "text/xml; charset=utf-8"
}


def null_val(s):
    if not s:
        s = 'NaN'
    else:
        s = s.group(1)
    return s


def null_des(s):
    if not s:
        s = ''
    else:
        s = s.group(1)
    return s


data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
    <soapenv:Header/>
    <soapenv:Body>
        <tem:getFood>
            <!--Optional:-->
            <tem:name></tem:name>
        </tem:getFood>
        </soapenv:Body>
        </soapenv:Envelope>"""
r = requests.post(url, data=data, headers=headers)
response = requests.post(url, data=data, headers=headers)
x = response.content.decode('utf-8')
food_name = []
ss_code = []
carbs = []
fat = []
fiber = []
sugar = []
sodium = []
alchohol = []
calorie = []
description = []
calorie_saturated_fats = []
image_path = []
protein = []
seqid = []
z = x.strip().split('Table')
fd_id = []

for i in range(3, len(z)):
    if(i % 3 == 0):
        # print(z[i])
        # print("\n")
        food_name.append(re.search('<FM_NAME>(.*)</FM_NAME>', z[i]).group(1))
        ss = re.search('<FM_SS_CODE>(.*)</FM_SS_CODE>', z[i])
        ss_code.append(null_val(ss))
        ss = (re.search('<FM_SEQID>(.*)</FM_SEQID>', z[i]).group(1))
        seqid.append(ss)
        ss = re.search('<FM_CARBOHYDRATE>(.*)</FM_CARBOHYDRATE>', z[i])
        carbs.append(null_val(ss))
        ss = re.search('<FM_FAT>(.*)</FM_FAT>', z[i])
        fat.append(null_val(ss))
        ss = re.search('<FM_FIBER>(.*)</FM_FIBER>', z[i])
        fiber.append(null_val(ss))
        ss = re.search('<FM_SUGAR>(.*)</FM_SUGAR>', z[i])
        sugar.append(null_val(ss))
        ss = re.search('<FM_SODIUM>(.*)</FM_SODIUM>', z[i])
        sodium.append(null_val(ss))
        ss = re.search('<FM_ALCHOHOL>(.*)</FM_ALCHOHOL>', z[i])
        alchohol.append(null_val(ss))
        ss = re.search('<FM_CALORIE>(.*)</FM_CALORIE>', z[i])
        calorie.append(null_val(ss))
        ss = re.search(
            '<FM_CALORIE_SATURATED_FATS>(.*)</FM_CALORIE_SATURATED_FATS>', z[i])
        calorie_saturated_fats.append(null_val(ss))
        ss = re.search('<FM_DESCRIPTION>(.*)</FM_DESCRIPTION>', z[i])
        description.append(null_des(ss))
        ss = re.search('<FM_PROTIN>(.*)</FM_PROTIN>', z[i])
        protein.append(null_val(ss))
        ss = re.search('<FM_IMAGEPATH>(.*)</FM_IMAGEPATH>', z[i])
        image_path.append(null_val(ss))


foodlist = pd.DataFrame()
foodlist['food_name'] = food_name
foodlist['description'] = description
foodlist['ss_code'] = ss_code
foodlist['carbs'] = carbs
foodlist['protein'] = protein
foodlist['fat'] = fat
foodlist['fiber'] = fiber
foodlist['sugar'] = sugar
foodlist['sodium'] = sodium
foodlist['alchohol'] = alchohol
foodlist['calorie'] = calorie
foodlist['calorie_saturated_fats'] = calorie_saturated_fats
foodlist['image_path'] = image_path
foodlist['seq_id'] = seqid
foodlist['image_path'] = foodlist['image_path'].apply(
    lambda x: x.replace('//', '/'))
foodlist['image_path'] = foodlist['image_path'].apply(
    lambda x: x.replace('http:/pancare.', 'http://tpancare.'))
fooddiary = pd.DataFrame()
fooddiary = foodlist[total_count:]


json_list = json.loads(json.dumps(list(fooddiary.T.to_dict().values())))
for dic in json_list:
    Food_diary_new.objects.get_or_create(**dic)
    print(dic['food_name'])


def north(request):
    north_indian = Food_diary_new.objects.all()
    paginator = Paginator(north_indian, 20)
    page = request.GET.get('page')
    try:
        north_indian = paginator.page(page)
    except PageNotAnInteger:
        north_indian = paginator.page(1)
    except EmptyPage:
        north_indian = paginator.page(page.num_pages)
    context_dict = {'north_indian': north_indian, 'page': page}
    return render(request, 'north.html', context=context_dict)


def search(request):
    query = request.GET['query']
    if len(query) > 100:
        allFood = Food_diary_new.objects.none()
    elif(query == ''):
        allFood = Food_diary_new.objects.none()
    else:
        allFood = Food_diary_new.objects.filter(food_name__icontains=query)
    if allFood.count() == 0:
        messages.error(request, "Please fill the correct food item")

    params = {'allFood': allFood, 'query': query}
    return render(request, 'search.html', params)


def purchase_card(request):
    return render(request, 'purchase_cards.html')

class purchase_cards_views(APIView):

    def get(self,request):
        queryset=purchase_cards.objects.all()
        serializers_class=Purchase_cards_serializer(queryset,many=True)
        return Response({'status':'SUCCESS','data':serializers_class.data},status=200)
class cuisine_fooditems_views(APIView):

    def get(self,request):
        queryset=Old_Food_Diary.objects.all()
        serializers_class=Cuisine_food_items_serializer(queryset,many=True)
        return Response({'status':'SUCESS','data': serializers_class.data},status=200)
class purchase_transactions_views(APIView):

    def post(self,request):
        userid=request.data.get('userid')
        from_date=request.data.get('from_date')
        to_date=request.data.get('to_date')
        #to_date=datetime.fromisoformat(to_date)
        #to_date=to_date+timedelta(day=1)
        combine_date=Purchase_det_new.objects.filter(Q(user_id=userid),Q(date__range=[from_date,to_date]))
        serializers=Purchase_transactions_serializer(data=combine_date,many=True)
        if serializers.is_valid():
            serializers.save()
        return Response({'status':'SUCESS','data': serializers.data},status=200)

class purchase_fooditem_views(APIView):

    def post(self,request):
        foodname=request.data.get('food_name')
        food_detail=purchase_cards.objects.filter(food_name=foodname)
        serializers=Purchase_fooditem_serializer(data=food_detail,many=True)
        if serializers.is_valid():
            serializers.save()
        return Response({'status':'SUCESS','data': serializers.data},status=200)


class cuisine_fooditem_views(APIView):

    def post(self,request):
        foodname=request.data.get('food_name')
        food_detail=Old_Food_Diary.objects.filter(food_name=foodname)
        serializers=Cuisine_fooditem_serializer(data=food_detail,many=True)
        if serializers.is_valid():
            serializers.save()
        return Response({'status':'SUCESS','data': serializers.data},status=200)

class cuisine_transactions_views(APIView):

    def post(self,request):
        userid=request.data.get('userid')
        from_date=request.data.get('from_date')
        to_date=request.data.get('to_date')
        combine_date=cuisine_consumption_det.objects.filter(Q(user_id=userid),Q(date__range=[from_date,to_date]))
        serializers=Cuisine_transactions_serializer(data=combine_date,many=True)
        if serializers.is_valid():
            serializers.save()
        return Response({'status':'SUCESS','data': serializers.data},status=200)