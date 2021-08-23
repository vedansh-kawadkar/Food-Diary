from os import linesep
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from numpy.core.arrayprint import printoptions
from pandas.core.frame import DataFrame
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
from rest_framework.views import APIView
from django.views.generic import View
from urllib.request import urlopen
from json import dumps
import json
import requests
from django.template import RequestContext
from FoodIndex_new.models import *
import matplotlib.pyplot as plt1
from django.db.models import Sum
import seaborn as sns
from matplotlib import pyplot as plt, use
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from home_app_new.models import Main_page
from basic_app_new.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from datetime import datetime, date
import datetime as dt
from django.urls import reverse
import mysql.connector as msql
import pandas as pd
import numpy as np
#from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
#from requests.api import request

# Create your views here.

quant = {}
det = {}
items = Food_diary_new.objects.all()

z = 0
x = 0
y = 0
w = 0
for i in items:
    quant[i.food_name] = 0

# function to authenticate user


def check_user(loginID, password):
    url = "http://tpancare.panhealth.com/panwebservicev1/Service.asmx?WSDL"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    data = """<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                      <soap:Body>
                        <getMemberinfo_json xmlns="http://tempuri.org/">
                          <strUserid>"""+str(loginID)+"""</strUserid>
                          <strPass>"""+str(password)+"""</strPass>
                        </getMemberinfo_json>
                      </soap:Body>
                    </soap:Envelope>"""

    response = requests.post(url, data=data, headers=headers)
    jsonobj = json.loads(response.content.decode(
        'utf-8').strip().split('<?xml')[0])
    if(jsonobj['Posts']):
        det['Firstname'] = jsonobj['Posts'][0]['ME_FIRSTNAME']
        det['Lastname'] = jsonobj['Posts'][0]['ME_LASTNAME']
        return 1
    else:
        return 0


def checker(s, z):
    if not re.search(s, z[3]):
        return 0
    else:
        return re.search(s, z[3]).group(1)

# function to get details of a particular food using food name


def get_food_details(f_name):
    url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    data = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <getFood xmlns="http://tempuri.org/">
        <name>"""+str(f_name)+"""</name>
        </getFood>
    </soap:Body>
    </soap:Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    response = requests.post(url, data=data, headers=headers)
    x = response.content.decode('utf-8')
    z = x.strip().split('Table')
    dic = {}
    dic['food_name'] = re.search('<FM_NAME>(.*)</FM_NAME>', z[3]).group(1)
    dic['ss_code'] = checker('<FM_SS_CODE>(.*)</FM_SS_CODE>', z)
    dic['fat'] = checker('<FM_FAT>(.*)</FM_FAT>', z)
    dic['fiber'] = checker('<FM_FIBER>(.*)</FM_FIBER>', z)
    dic['sugar'] = checker('<FM_SUGAR>(.*)</FM_SUGAR>', z)
    dic['sodium'] = checker('<FM_SODIUM>(.*)</FM_SODIUM>', z)
    dic['alchohol'] = checker('<FM_ALCHOHOL>(.*)</FM_ALCHOHOL>', z)
    dic['calorie'] = checker('<FM_CALORIE>(.*)</FM_CALORIE>', z)
    dic['calorie_saturated_fat'] = checker(
        '<FM_CALORIE_SATURATED_FATS>(.*)</FM_CALORIE_SATURATED_FATS>', z)
    dic['protein'] = checker('<FM_PROTIN>(.*)</FM_PROTIN>', z)
    dic['carbs'] = checker('<FM_CARBOHYDRATE>(.*)</FM_CARBOHYDRATE>', z)
    dic['f_id'] = checker('<FM_SEQID>(.*)</FM_SEQID>', z)
    dic['image_link'] = checker('<FM_IMAGEPATH>(.*)</FM_IMAGEPATH>', z)
    return dic


def checkemail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False


def home(request):
    if request.method == "POST":
        user = request.POST['userId']
        # checkemail(user)
        if checkemail(email=user):
            messages.error(request, "Please Enter Valid 'User ID'.")
            return redirect("/")

        pwd = request.POST['pwd']

        result = check_user(user, pwd)

        global w
        w = w+1
        if w == 1:
            try:
                unsav = Unsaved_new.objects.all()
                for i in unsav:
                    if(i.user_id == user):
                        entry = Temporary_new(
                            user_id=user,
                            food_name=i.food_name,
                            quantity=i.quantity,
                            mfg_code=i.mfg_code,
                            meal_type=i.meal_type,
                            ss_code=i.ss_code,
                            Food_id=i.Food_id,
                            carbs=i.carbs,
                            protein=i.protein,
                            fat=i.fat,
                            fiber=i.fiber,
                            sugar=i.sugar,
                            sodium=i.sodium,
                            alchohol=i.alchohol,
                            calorie=i.calorie,
                            calorie_saturated_fats=i.calorie_saturated_fats)
                        entry.save()
                        i.delete()
                uns = Unsaved_purchase_new.objects.all()
                for j in uns:
                    if(j.user_id == user):
                        ent = Temporary_purchase_new(
                            user_id=user,
                            mfg_code=j.mfg_code,
                            food_name=j.food_name,
                            quantity=j.quantity,
                            ss_code=j.ss_code,
                            Food_id=j.Food_id,
                            carbs=j.carbs,
                            protein=j.protein,
                            fat=j.fat,
                            fiber=j.fiber,
                            sugar=j.sugar,
                            sodium=j.sodium,
                            alchohol=j.alchohol,
                            calorie=j.calorie,
                            calorie_saturated_fats=j.calorie_saturated_fats,
                            shop_name=j.shop_name)
                        ent.save()

                    else:
                        continue

            except Unsaved_new.DoesNotExist:
                item = None

        if result == 0:
            messages.error(request, "Invalid UserId or Password!")
            return redirect('/')
        else:
            if User.objects.filter(username = user).exists():
                user_id = authenticate(username=user,password=pwd)
                login(request,user_id)
            else:
                new_entry = User(
                    username = user,
                    first_name = det['Firstname'],
                    last_name = det['Lastname'],
                )
                new_entry.set_password(pwd)
                new_entry.save()
                user_id = authenticate(request,username=user,password=pwd)
                login(request,user_id)
            
            current_user = request.user
            request.session['user'] = current_user.username
          
            allTypes = Main_page.objects.all()
            con = {'allTypes': allTypes}
            return render(request, 'home.html', con)
    else:

        return render(request, 'home.html')


'''def renderhome(request):
    return render(request,'home.html')'''


def details(request, f_name):

    food_det = get_food_details(f_name)
    img_url = food_det['image_link']
    img_url = img_url.replace('//', '/')
    img_url = img_url.replace('http:/pancare.', 'http://tpancare.')
    return render(request, 'details.html', {'info': food_det, 'food_name': f_name, 'image_link': img_url})


def add_item1(request):
    user_id = request.user
    print(user_id)
    print('a')
    print(user_id)
    user = user_id.username
    print(user)
    if request.method == "POST":
        meal = request.POST["meal_type"]
        f_name = request.POST["item"]
        seq_id = request.POST["seqid"]
        qnt = request.POST["selectedQuant"]
        dic = {}
        dic = get_food_details(seq_id)
        f_id = dic['f_id']
        cal = dic['calorie']
        prot = dic['protein']
        fat = dic['fat']
        fiber = dic['fiber']
        carbs = dic['carbs']
        sat = dic['calorie_saturated_fat']
        sod = dic['sodium']
        sug = dic['sugar']
        alc = dic['alchohol']
        ss_c = dic['ss_code']
        prot = float(prot)
        fat = float(fat)
        fiber = float(fiber)
        carbs = float(carbs)
        sat = float(sat)
        sod = float(sod)
        sug = float(sug)
        alc = float(alc)
        cal = float(cal)
        num = float(qnt)
        new_entry = Temporary_new(
            user_id=user,
            food_name=f_name,
            quantity=qnt,
            meal_type=meal,
            ss_code=ss_c,
            Food_id=f_id,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num
        )
        new_entry.save()
        return redirect('/north')


def table(request):
    user_id = request.user
    user = user_id.username
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
        item = Temporary_new.objects.filter(user_id=user)
    except Temporary_new.DoesNotExist:
        item = None

    return render(request, 'table.html', {'info': item, 'name': name, 'date_time': d1})


def purchase(request):
    user_id = request.user
    print(user_id)
    print('a')
    user = user_id.username
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y %H:%M:%S")
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    try:
        item = Temporary_purchase_new.objects.filter(user_id=user)
    except Temporary_purchase_new.DoesNotExist:
        item = None

    return render(request, 'purchase.html', {'info': item, 'name': name, 'date_time': d1})


def confirm_purchase(request):
    user_id = request.user
    user = user_id.username
    if request.method == "POST":
        f_name = request.POST["selectedItem2"]
        qnt = request.POST["selectedQuant"]
        shop = request.POST["shop"]
        seq_id = request.POST["sq"]
        items = purchase_cards.objects.get(id=seq_id)
        prot = float(items.protein)
        fat = float(items.fat)
        fiber = float(items.fiber)
        carbs = float(items.carbs)
        sat = float(items.calorie_saturated_fats)
        sod = float(items.sodium)
        sug = float(items.sugar)
        alc = float(items.alcohol)
        cal = float(items.calorie)
        num = int(qnt)
        new_entry = Temporary_purchase_new(
            user_id=user,
            food_name=f_name,
            quantity=qnt,
            ss_code=items.ss_code,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num,
            shop_name=shop
        )

        new_entry.save()
        try:
            item = Temporary_purchase_new.objects.all()
        except Temporary_purchase_new.DoesNotExist:
            item = None
        if shop == "Bigbasket":
            return redirect('/bb')
        elif shop == "amazon":
            return redirect('/amazon')
        elif shop == "Grofers":
            return redirect('/grofers')
        else:
            return redirect('/purchase')


def other_purchase(request):
    user_id = request.user
    user = user_id.username
    if request.method == "POST":
        f_name = request.POST["selectedItem3"]
        qnt = request.POST["selectedQuant3"]
        shop = request.POST["vendor_name3"]
        seq_id = request.POST["sq3"]
        items = purchase_cards.objects.get(id=seq_id)
        prot = float(items.protein)
        fat = float(items.fat)
        fiber = float(items.fiber)
        carbs = float(items.carbs)
        sat = float(items.calorie_saturated_fats)
        sod = float(items.sodium)
        sug = float(items.sugar)
        alc = float(items.alcohol)
        cal = float(items.calorie)
        num = int(qnt)
        new_entry = Temporary_purchase_new(
            user_id=user,
            food_name=f_name,
            quantity=qnt,
            ss_code=items.ss_code,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num,
            shop_name=shop
        )

        new_entry.save()
        try:
            item = Temporary_purchase_new.objects.all()
        except Temporary_purchase_new.DoesNotExist:
            item = None

        return redirect('/others')


def confirm_purchase2(request):
    user_id = request.user
    user = user_id.username
    if request.method == "POST":
        f_name = request.POST["selectedItem"]
        m = request.POST["mfg"]
        cal = request.POST["cal"]
        fat = request.POST["fat"]
        prot = request.POST["protin"]
        carbs = request.POST["carbs"]
        qnt = request.POST["quantity"]
        fiber = request.POST["fiber"]
        sat = request.POST["sat"]
        sod = request.POST["sodium"]
        sug = request.POST["sugar"]
        alc = request.POST["alc"]
        ss_c = request.POST["ss_c"]
        vendor_name = request.POST["vendor_name1"]
        prot = int(prot)
        fat = int(fat)
        fiber = int(fiber)
        carbs = int(carbs)
        sat = int(sat)
        sod = int(sod)
        sug = int(sug)
        alc = int(alc)
        cal = int(cal)
        num = int(qnt)
        new_entry = Temporary_purchase_new(
            user_id=user,
            food_name=f_name,
            mfg_code=m,
            quantity=qnt,
            ss_code=ss_c,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num,
            shop_name=vendor_name
        )

        new_entry.save()
        try:
            item = Temporary_purchase_new.objects.all()
        except Temporary_purchase_new.DoesNotExist:
            item = None

        if vendor_name == "Bigbasket":
            return redirect('/bb')
        elif vendor_name == "amazon":
            return redirect('/amazon')
        elif vendor_name == "Grofers":
            return redirect('/grofers')
        else:
            return redirect('/others')


def delete(request, f_name):
    user_id = request.user
    user = user_id.username
    instance = Temporary_new.objects.get(food_name=f_name)
    instance.delete()
    unsav = Unsaved_new.objects.all()
    tod = datetime.date(datetime.now())
    for i in unsav:
        if(i.user_id == user and i.date == tod and i.food_name == f_name):
            i.delete()
    quant[f_name] = 0
    try:
        item = Temporary_new.objects.all()
        return redirect('/table')
    except Temporary_new.DoesNotExist:
        return redirect('/home')


def delete_purchase(request, f_id):
    user_id = request.user
    user = user_id.username
    f_id = int(f_id)
    instance = Temporary_purchase_new.objects.get(Food_id=f_id)
    shop = instance.shop_name
    instance.delete()
    unsav = Unsaved_purchase_new.objects.all()
    tod = datetime.date(datetime.now())

    for i in unsav:
        if(i.user_id == user and i.Food_id == f_id):
            i.delete()

    try:
        item = Temporary_purchase_new.objects.all()
        if shop == "Bigbasket":
            return redirect('/bb')
        elif shop == "amazon":
            return redirect('/amazon')
        elif shop == "Grofers":
            return redirect('/grofers')
        else:
            return redirect('/others')
    except Temporary_purchase_new.DoesNotExist:
        return redirect('/home')


def delete_purchase2(request, f_id):
    user_id = request.user
    user = user_id.username
    f_id = int(f_id)
    instance = Temporary_purchase_new.objects.get(Food_id=f_id)
    shop = instance.shop_name
    instance.delete()
    unsav = Unsaved_purchase_new.objects.all()
    tod = datetime.date(datetime.now())

    for i in unsav:
        if(i.user_id == user and i.Food_id == f_id):
            i.delete()

    try:
        item = Temporary_purchase_new.objects.all()
        return redirect('/purchase')
    except Temporary_purchase_new.DoesNotExist:
        return redirect('/home')

# function to store consumption details into pancare userlog


def store_pancare(userID, f_name, date, time, meal, ss_c, qnt, cal):
    url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    data2 = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <FoodLog xmlns="http://tempuri.org/">
        <ME_ID>"""+str(userID)+"""</ME_ID>
        <Date>"""+str(date)+"""</Date>
        <Time>"""+str(time)+"""</Time>
        <Food_Name>"""+str(f_name)+"""</Food_Name>
        <Mealtype>"""+str(meal)+"""</Mealtype>
        <Serving_Style>"""+str(ss_c)+"""</Serving_Style>
        <Food_Quntity>"""+str(qnt)+"""</Food_Quntity>
        <Food_Calorie>"""+str(cal)+"""</Food_Calorie>
        <timezone></timezone>
        </FoodLog>
    </soap:Body>
    </soap:Envelope>"""
    r = requests.post(url, data=data2, headers=headers)


def save_table(request):
    user_id = request.user
    user = user_id.username

    try:
        item = Temporary_new.objects.all()

        for i in item:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            tod = datetime.date(datetime.now())
            store_pancare(user, i.food_name, tod, current_time,
                          i.meal_type, i.ss_code, i.quantity, i.calorie)
            entry = Transaction_det_new(
                user_id=user,
                date=tod,
                mfg_code=i.mfg_code,
                time_rec=current_time,
                food_name=i.food_name,
                quantity=i.quantity,
                meal_type=i.meal_type,
                ss_code=i.ss_code,
                Food_id=i.Food_id,
                carbs=i.carbs,
                protein=i.protein,
                fat=i.fat,
                fiber=i.fiber,
                sugar=i.sugar,
                sodium=i.sodium,
                alchohol=i.alchohol,
                calorie=i.calorie,
                calorie_saturated_fats=i.calorie_saturated_fats)

            entry.save()
            Temporary_new.objects.all().delete()
            unsav = Unsaved_new.objects.all()
            tod = datetime.date(datetime.now())
            for i in unsav:
                if(i.user_id == user and i.date == tod):
                    i.delete()
        return redirect('/home')

    except Transaction_det_new.DoesNotExist:
        return redirect('/home')


def save_purchase(request):
    user_id = request.user
    user = user_id.username
    try:
        item = Temporary_purchase_new.objects.all()

        for i in item:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            entry = Purchase_det_new(
                user_id=user,
                date=datetime.date(datetime.now()),
                mfg_code=i.mfg_code,
                time_rec=current_time,
                food_name=i.food_name,
                quantity=i.quantity,
                ss_code=i.ss_code,
                carbs=i.carbs,
                protein=i.protein,
                fat=i.fat,
                fiber=i.fiber,
                sugar=i.sugar,
                sodium=i.sodium,
                alchohol=i.alchohol,
                calorie=i.calorie,
                calorie_saturated_fats=i.calorie_saturated_fats,
                shop_name=i.shop_name)

            entry.save()
            Temporary_purchase_new.objects.all().delete()
            unsav = Unsaved_purchase_new.objects.all()
            tod = datetime.date(datetime.now())
            for i in unsav:
                if(i.user_id == user and i.date == tod):
                    i.delete()
        return redirect('/home')

    except Transaction_det_new.DoesNotExist:
        return redirect('/home')


def deletetemp(request):
    global w
    try:
        user_id = request.user
        user = user_id.username
        items = Temporary_new.objects.all()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        for i in items:
            quant[i.food_name] = 0
            entry = Unsaved_new(
                user_id=user,
                date=datetime.date(datetime.now()),
                time_rec=current_time,
                food_name=i.food_name,
                quantity=i.quantity,
                meal_type=i.meal_type,
                ss_code=i.ss_code,
                Food_id=i.Food_id,
                carbs=i.carbs,
                protein=i.protein,
                fat=i.fat,
                fiber=i.fiber,
                sugar=i.sugar,
                sodium=i.sodium,
                alchohol=i.alchohol,
                calorie=i.calorie,
                calorie_saturated_fats=i.calorie_saturated_fats)

            entry.save()

        it = Temporary_purchase_new.objects.all()

        for j in it:
            entry = Unsaved_purchase_new(
                user_id=user,
                date=datetime.date(datetime.now()),
                time_rec=current_time,
                food_name=j.food_name,
                quantity=j.quantity,
                ss_code=j.ss_code,
                Food_id=j.Food_id,
                carbs=j.carbs,
                protein=j.protein,
                fat=j.fat,
                fiber=j.fiber,
                sugar=j.sugar,
                sodium=j.sodium,
                alchohol=j.alchohol,
                calorie=j.calorie,
                calorie_saturated_fats=j.calorie_saturated_fats,
                shop_name=j.shop_name)

            entry.save()
        w = 0
        Temporary_new.objects.all().delete()
        Temporary_purchase_new.objects.all().delete()
        logout(request)
        return HttpResponseRedirect('/')
    except Temporary_new.DoesNotExist:
        w = 0
        logout(request)
        return HttpResponseRedirect('/')


def profile_page(request):
    user_id = request.user
    user = user_id.username
    first = user_id.first_name
    last = user_id.last_name
    name = str(first) +' '+ str(last)
    return render(request, 'profile_page.html', {'name': name, 'user': user})


def userfoodlogchart(request):
    user = request.user
    user_id = user.username
    url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
    <soapenv:Header/>
    <soapenv:Body>
        <tem:GetUserFoodLog>
            <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
            <tem:FoodName></tem:FoodName>
            <tem:fromDate></tem:fromDate>
            <tem:toDate></tem:toDate>
        </tem:GetUserFoodLog>
    </soapenv:Body> 
    </soapenv:Envelope>"""

    response = requests.post(url, data=data2, headers=headers)

    x = response.content.decode('utf-8')
    z = x.strip().split('Table')

    food_name = []
    date = []
    quantity = []
    calorie = []
    meal_type = []
    time = []

    for i in range(3, len(z)):
        if(i % 3 == 0):
            food_name.append(
                re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
            date.append(
                re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
            quantity.append(
                re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
            calorie.append(
                re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
            meal_type.append(
                re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
            time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

    user_log = pd.DataFrame()
    user_log['food_name'] = food_name
    user_log['date'] = date
    user_log['time'] = time
    user_log['quantity'] = quantity
    user_log['calorie'] = calorie
    user_log['meal_type'] = meal_type
    # print(user_log)
    today = datetime.strptime(
        str(dt.date.today()), '%Y-%m-%d').strftime('%m/%d/%Y')
    # print(today)

    pie_df = user_log[user_log.date == today]

    alldata = []
    for i in range(pie_df.shape[0]):
        temp = pie_df.iloc[i]
        alldata.append(dict(temp))
    alldata = dumps(alldata)
    # print(alldata)

    if request.method == 'POST':
        fromdate = request.POST["fromdate"]
        if fromdate == "":
            messages.warning(request, "Please Enter 'From' Date.")
            return redirect("/home/userfoodlogchart")
        else:
            fromdate = pd.to_datetime(fromdate)

        todate = request.POST["todate"]
        if todate == "":
            todate = pd.to_datetime(dt.datetime.today())
            print(todate)
        else:
            todate = pd.to_datetime(todate)

        if fromdate > todate:
            messages.warning(request, "Mismatch Of Dates!!!")
            return redirect("/home/userfoodlogchart")

        mealtype = request.POST["mealtype"]
        print(mealtype)
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body> 
        </soapenv:Envelope>"""

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type
        user_log["date"] = pd.to_datetime(user_log['date'])

        if mealtype == 'all' or mealtype == "Select":
            chart_df = user_log[((user_log.date >= fromdate)
                                 & (user_log.date <= todate))]
            dateset = sorted(set(chart_df["date"]))
            calorie_sums = []
            for i in range(len(dateset)):
                numcal = sum(pd.to_numeric(
                    chart_df[(chart_df.date == dateset[i])]['calorie']))
                calorie_sums.append(numcal)

            alldates = []
            for d in dateset:
                alldates.append(str(d.date()))

            cal_list = list(zip(alldates, calorie_sums))
            # print(cal_list)
            s = ["date", "sum"]
            mw = {"min. calories req. for men": 2000,
                  "min. calories req. for women": 1600}
            cal_data = []

            for i in range(len(alldates)):
                a = dict(zip(s, list(cal_list[i])))
                a.update(mw)
                cal_data.append(a)
            # print(cal_data)
            cal_data = dumps(cal_data)
            # print(cal_data)

            return render(request, 'userfoodlogchart.html', context={"cal_data": cal_data, "data": alldata, "fromdate": fromdate, "todate": todate})

        else:
            chart_df = user_log[((user_log.date >= fromdate) & (
                user_log.date <= todate)) & (user_log.meal_type == mealtype)]
            dateset = sorted(set(chart_df["date"]))
            # print(dateset)
            calorie_sums = []
            bfcals = []
            lunchcals = []
            snackscals = []
            dinnercals = []

            for i in range(len(dateset)):
                numcal = sum(pd.to_numeric(
                    chart_df[(chart_df.date == dateset[i])]['calorie']))
                calorie_sums.append(numcal)

            # print(calorie_sums)

            alldates = []
            for d in dateset:
                alldates.append(str(d.date()))
            # print(alldates)

            cal_list = list(zip(alldates, calorie_sums))
            # print(cal_list)
            s = ["date", "sum"]
            mw = {"min. calories req. for men": 2000,
                  "min. calories req. for women": 1600}
            cal_data = []
            for i in range(len(alldates)):
                a = dict(zip(s, list(cal_list[i])))
                a.update(mw)
                cal_data.append(a)
            # print(cal_data)
            cal_data = dumps(cal_data)
            # print(cal_data)

            return render(request, 'userfoodlogchart.html', context={"cal_data": cal_data, "data": alldata})

    return render(request, 'userfoodlogchart.html', context={"data": alldata})


def foodtopan(request):
    user_id = request.user
    user = user_id.username
    if request.method == "POST":
        f_name = request.POST.get("selectedItem")
        desc = request.POST.get("desc")
        m = request.POST.get("mfg")
        f_id = request.POST.get("fd_id")
        cal = request.POST.get("cal")
        fat = request.POST.get("fat")
        prot = request.POST.get("protin")
        carbs = request.POST.get("carbs")
        qnt = request.POST.get("quantity")
        fiber = request.POST.get("fiber")
        sat = request.POST.get("sat")
        sod = request.POST.get("sodium")
        sug = request.POST.get("sugar")
        alc = request.POST.get("alc")
        ss_c = request.POST.get("ss_c")
        sat = request.POST.get("sat")
        meal = request.POST.get("meal_type")

        prot = float(prot)
        fat = float(fat)
        fiber = float(fiber)
        carbs = float(carbs)
        sat = float(sat)
        sod = float(sod)
        sug = float(sug)
        alc = float(alc)
        cal = float(cal)
        num = float(qnt)
        new_entry = Temporary_new(
            user_id=user,
            food_name=f_name,
            quantity=qnt,
            meal_type=meal,
            ss_code=ss_c,
            Food_id=f_id,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num
        )
        new_entry.save()
        print(carbs, fat, prot)

        url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
        headers = {"Content-Type": "text/xml; charset=utf-8"}

        data2 = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <AddFood xmlns="http://tempuri.org/">
            <ME_ID>"""+str(user)+"""</ME_ID>
            <Name>"""+str(f_name)+"""</Name>
            <Description>"""+str(desc)+"""</Description>
            <ss_code>"""+str(ss_c)+"""</ss_code>
            <Protin>"""+str(prot)+"""</Protin>
            <Carbohydrate>"""+str(carbs)+"""</Carbohydrate>
            <Fat>"""+str(fat)+"""</Fat>
            <Fiber>"""+str(fiber)+"""</Fiber>
            <Sugar>"""+str(sug)+"""</Sugar>
            <Sodium>"""+str(sod)+"""</Sodium>
            <Alchohol>"""+str(alc)+"""</Alchohol>
            <Calorie>"""+str(cal)+"""</Calorie>
            <Calorie_saturated_fats>"""+str(sat)+"""</Calorie_saturated_fats>
            </AddFood>
        </soap:Body>
        </soap:Envelope>"""
        print(data2)

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')
        print(z[0])
        if "true" in z[0]:
            messages.success(
                request, f"Food Item:{f_name} added successfully to PAN!!")
        elif "false" in z[0]:
            messages.error(request, f"Can not add food item.")

        return redirect("/home/table")


calx = []
listdate = []


def null_val(s):
    if not s:
        s = '0'
    else:
        s = s.group(1)
    return s


def chartof(request):
    user_id = request.user
    user = user_id.username
    if request.method == 'POST':
        if(len(calx) > 0):
            del calx[:]
        nuttype = str(request.POST['charts'])
        # datex=str(request.POST['fromdate'])
        dateobj = request.POST["fromdate"]
        nd = datetime.strptime(dateobj, '%Y-%m-%d')
        newdate = datetime.strptime(dateobj, '%Y-%m-%d').strftime('%m/%d/%Y')
        curr_date = str(newdate)
        print(newdate)

        url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body>
        </soapenv:Envelope>"""
        resp = requests.post(url, data=data2, headers=headers)
        x = resp.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        for i in range(0, len(calorie)):
            calorie[i] = int(calorie[i])
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type

        prev_date = dt.date.today() - dt.timedelta(days=1)
        d4 = dt.date.strftime(prev_date, "%m/%d/%Y")

        if(len(calx) > 0):
            del calx[:]

        for i in range(5):
            prev_date = nd - dt.timedelta(days=i)
            d4 = dt.date.strftime(prev_date, "%m/%d/%Y")
            # print(d4)

            listdate.append(d4)
        # print(listdate)
        listof = []
        cal = ''
        calex = ''
        if(nuttype == 'calorie'):
            cal = '<FM_CALORIE>'
            calex = '</FM_CALORIE>'
        elif(nuttype == 'carbohydrate'):
            cal = '<FM_CARBOHYDRATE>'
            calex = '</FM_CARBOHYDRATE>'
        elif(nuttype == 'sodium'):
            cal = '<FM_SODIUM>'
            calex = '</FM_SODIUM>'
        elif(nuttype == 'sugar'):
            cal = '<FM_SUGAR>'
            calex = '</FM_SUGAR>'
        elif(nuttype == 'alcohol'):
            cal = '<FM_ALCHOHOL>'
            calex = '</FM_ALCHOHOL>'
        elif(nuttype == 'fiber'):
            cal = '<FM_FIBER>'
            calex = '</FM_FIBER>'
        else:
            cal = '<FM_FAT>'
            calex = '</FM_FAT>'

        nutdata = []

        for i in user_log['food_name']:
            strin = i
            # print(strin)
            data = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <getFood xmlns="http://tempuri.org/">
                    <name>"""+str(strin)+"""</name>
                    </getFood>
                </soap:Body>
                </soap:Envelope>"""
            r = requests.post(url, data=data, headers=headers)
            response = requests.post(url, data=data, headers=headers)
            x = response.content.decode('utf-8')
            z = x.strip().split('Table')
            ss = re.search(cal+'(.*)'+calex, z[3])
            nutdata.append(null_val(ss))

        for i in range(0, len(nutdata)):
            nutdata[i] = float(nutdata[i])*int(user_log['quantity'][i])
            # print(nutdata[i])
        user_log['nutdata'] = nutdata
        for i in listdate:
            dfxx = user_log[user_log['date'] == i]
            cali = np.sum(dfxx['nutdata'])
            calx.append(cali)
        fromdate = listdate[-1]
        todate = listdate[-5]
        cont = {'nuttype': nuttype, 'fromdate': fromdate, 'todate': todate}
        return render(request, 'index.html', cont)
    else:
        return render(request, 'index.html')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = listdate[-5:]
        chartLabel = "Total Nutrition per day"
        chartdata = calx[-5:]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }

        return Response(data)


def purchase_status(request):
    if request.method=="POST":
        select_from=request.POST['fromdate']
        select_to=request.POST['todate']
        user1 = request.user
        user_id = user1.username
        combine_date=Purchase_det_new.objects.filter(user_id=user_id,date__range=[select_from, select_to]).order_by('date')
        con={'combine_date':combine_date}
        return render(request,'purchase_status.html',con)

    else:
        user1 = request.user
        user_id = user1.username
        
        print(user_id)
        print(date.today())
        dates=date.today()
        all_objects = Purchase_det_new.objects.filter(user_id=user_id,date=dates).order_by('-date')
        print(all_objects)
        '''
        all_obj = Purchase_det_new.objects.all()
        df = pd.DataFrame(all_objects)
    
        dfz = df[df['user_id'] == user_id]
        dfz.drop('Food_id', inplace=True, axis='columns')
        dfz.drop('food_type', inplace=True, axis='columns')
        dfz.drop('calorie_saturated_fats', inplace=True, axis='columns')
        dfz.drop('ss_code', inplace=True, axis='columns')
        dfz.drop('alchohol', inplace=True, axis='columns')
        dfz.drop('sodium', inplace=True, axis='columns')
        dfz.drop('user_id', inplace=True, axis='columns')
        # print(dfz)
        '''
        con = {'all_objects': all_objects,}
        return render(request, 'purchase_status.html', con)


def purchasechart(request):
    if request.method == 'POST':
        user1 = request.user
        user_id = user1.username
        all_objects = Purchase_det_new.objects.all().values()
        all_obj = Purchase_det_new.objects.all()
        df = pd.DataFrame(all_objects)
        dfz = df[df['user_id'] == user_id]

        def func(date):
            return datetime.strftime(date, '%Y-%m-%d')

        def func2(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        dfz['date'] = dfz['date'].apply(func)
        # print(dfz['date'])
        purchaseset = list(set(list(dfz["food_name"])))
        # print(dfz)
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body> 
        </soapenv:Envelope>"""

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type
        print(user_log)
        consumeset = list(set(list(user_log["food_name"])))
        # print(consumeset)
        # print(purchaseset)
        fromdate = request.POST["fromdate"]
        #frmjson = []

        todate = request.POST["todate"]
        #tojson = []

        datevals = [{"fromd": fromdate}, {"tod": todate}]

        newdate1 = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%m/%d/%Y')
        newdate2 = datetime.strptime(todate, '%Y-%m-%d').strftime('%m/%d/%Y')

        if newdate1 > newdate2:
            messages.warning(request, "Mismatch Of Dates!!!")
            return redirect("/home/purchasechart")

        food_quantity = ["food_name", "quantity"]

        purchasedata = []
        pdata = []
        for i in purchaseset:
            dfz2 = dfz[((dfz.date >= fromdate) & (
                dfz.date <= todate)) & (dfz.food_name == i)]
            sums = sum(list(map(int, list(dfz2["quantity"]))))
            pdata.append([i, sums])
        for i in range(len(pdata)):
            purchasedata.append(dict(zip(food_quantity, pdata[i])))
        purchasedata = dumps(purchasedata)
        print(purchasedata)

        consumedata = []
        cdata = []
        for i in consumeset:
            consumedf = user_log[(user_log.date <= newdate2)
                                 & (user_log.date >= newdate1)]
            consumedf = consumedf[(user_log.food_name == i)]
            #print(consumedf["food_name"], consumedf["quantity"])
            sums = sum(list(map(int, list(consumedf["quantity"]))))
            cdata.append([i, sums])
        for i in range(len(cdata)):
            consumedata.append(dict(zip(food_quantity, cdata[i])))
        consumedata = dumps(consumedata)
        print(consumedata)

        return render(request, 'purchasechart.html', context={"consumedata": consumedata, "purchasedata": purchasedata, "fromdate": fromdate, "todate": todate})
    else:
        return render(request, "purchasechart.html")


def otherdayanalysis(request):
    if request.method == 'POST':
        user1 = request.user
        user_id = user1.username
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }
        dateobj = request.POST["dateinput2"]
        if dateobj == '':
            messages.warning(request, "Please Enter Date.")
            return redirect("/home/userdate_form")
        newdate = datetime.strptime(dateobj, '%Y-%m-%d').strftime('%m/%d/%Y')
        newdate = str(newdate)
        mealtype = request.POST["mealtype2"]

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body> 
        </soapenv:Envelope>"""

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type

        dateset = sorted(set(user_log['date']))
        if mealtype != "all" and mealtype != "Select":
            chart_df = user_log[(user_log.date == newdate)
                                & (user_log.meal_type == mealtype)]
            alldata = []
            #caloriesum = pd.to_numeric(chart_df["calorie"]).sum()
            for i in range(chart_df.shape[0]):
                temp = chart_df.iloc[i]
                alldata.append(dict(temp))
            alldata = dumps(alldata)

            return render(request, 'userdate_form.html', context={"alldata": alldata})

        else:
            chart_df = user_log[(user_log.date == newdate)]
            alldata = []

            for i in range(chart_df.shape[0]):
                temp = chart_df.iloc[i]
                alldata.append(dict(temp))
            alldata = dumps(alldata)
            context = {"data": alldata}

            return render(request, 'userdate_form.html', context={"alldata": alldata})
    else:
        return render(request, 'userdate_form.html')


def consumer_history(request):

    if request.method=="POST":
        user1 = request.user
        user_id = user1.username
        select_from=request.POST['fromdate']
        select_to=request.POST['todate']
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx?WSDL"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }
        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
    <soapenv:Header/>
    <soapenv:Body>
        <tem:GetUserFoodLog>
            <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
            <tem:FoodName></tem:FoodName>
            <tem:fromDate>"""+str(select_from)+"""</tem:fromDate>
            <tem:toDate>"""+str(select_to)+"""</tem:toDate>
        </tem:GetUserFoodLog>
    </soapenv:Body>
        </soapenv:Envelope>"""
        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')
        food_name = []
        date= []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                # print(z[i])
                # print("\n")
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))
        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type
        print(user_log['date'])
        #print(dt.date.today())
       
       
        #user_log=user_log[(user_log['date']>= select_from) & (user_log['date']<= select_to)]
        #user_log=pd.date_range(select_from,select_to)
        #user_log['date'] = pd.to_datetime(user_log['date'])
        #user_log[user_log.some_date.between(select_from,select_to)]  
       # user_log=user_log[user_log['date'].isin(pd.date_range('07-07-2021', '07-17-2021'))]
        #print(user_log)

        user_log = user_log.sort_values('date', ascending=True)
        print(user_log.head())
        p=True

        con = {'user_log': user_log,'p':p}
        return render(request, 'consumer_history.html', con)

    else:
        user1 = request.user
        user_id = user1.username
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx?WSDL"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }
        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
    <soapenv:Header/>
    <soapenv:Body>
        <tem:GetUserFoodLog>
            <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
            <tem:FoodName></tem:FoodName>
            <tem:fromDate></tem:fromDate>
            <tem:toDate></tem:toDate>
        </tem:GetUserFoodLog>
    </soapenv:Body>
        </soapenv:Envelope>"""
        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')
        food_name = []
        date= []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                # print(z[i])
                # print("\n")
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))
        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type
       # print(user_log['date'])
        #print(dt.date.today())
        today=dt.date.strftime(dt.date.today(), "%m/%d/%Y")
       # print(today)
        user_log=user_log[user_log['date']==today]
        

        user_log = user_log.sort_values('date', ascending=False)
        

        con = {'user_log': user_log}
        return render(request, 'consumer_history.html', con)



def purchaseComparison(request):
    myconn = msql.connect(host="15.207.8.17", user="Food",
                          password="zhTnxpRFiSzpaF2J", db='Food')
    concursor = myconn.cursor()

    db = """SELECT * FROM basic_app_new_purchase_det_new"""
    table = pd.read_sql(db, myconn)

    def func(d):
        return str(d)

    def func2(d):
        return float(d)

    table["date"] = table["date"].apply(func)
    table["carbs"] = table["carbs"].apply(func2)
    table["fat"] = table["fat"].apply(func2)
    table["fiber"] = table["fiber"].apply(func2)
    table["alchohol"] = table["alchohol"].apply(func2)
    table["sugar"] = table["sugar"].apply(func2)
    table["sodium"] = table["sodium"].apply(func2)
    table["calorie"] = table["calorie"].apply(func2)
    table["protein"] = table["protein"].apply(func2)
    today = dt.date.today()
    user1 = request.user
    user_id = user1.username

    user_df = table[table.user_id == user_id]
    print("******************User DF****************")
    print(user_df)

    prev_date = today - dt.timedelta(days=7)

    today_df = user_df[user_df.date == str(today)]
    print("********************Today DF*******************")
    print(today_df)
    week_df = user_df[(user_df.date <= str(today)) &
                      (user_df.date >= str(prev_date))]
    print("***************Week DF***************")
    print(week_df)
    today_overall_df = table[table.date == str(today)]
    print('************************Overall DF')
    print(today_overall_df)
    cols = ["todaynutrient", "todayquantity"]
    nutrients = ["carbs", "protein", "fat", "fiber",
                 "sodium", "alchohol", "sugar", "calorie"]
    sums = []
    nutrients_sum1 = []
    for i in nutrients:
        sums.append(sum(list(today_df[i])))
    for i in range(len(nutrients)):
        nutrients_sum1.append(dict(zip(cols, [nutrients[i], sums[i]])))
    nutrients_sum1 = dumps(nutrients_sum1)
    print(nutrients_sum1)

    cols2 = ["weeknutrient", "weekquantity"]
    #nutrients2 = ["carbs", "protein", "fat", "fiber", "sodium", "alchohol", "sugar", "calorie"]
    sums2 = []
    nutrients_sum2 = []
    for i in nutrients:
        sums2.append(sum(list(week_df[i])))
    # print(sums2)
    for i in range(len(nutrients)):
        nutrients_sum2.append(dict(zip(cols2, [nutrients[i], sums2[i]])))
    nutrients_sum2 = dumps(nutrients_sum2)
    print(nutrients_sum2)

    avg_calorie = 1800
    # print(nutrients_sum2)
    nutrients2 = ["carbs", "protein", "fat",
                  "fiber", "sodium", "alchohol", "sugar"]
    today_cal = sum(list(today_df["calorie"]))
    print(today_cal)
    week_cal = sums2[-1]/7
    today_cal_perc = ((abs(today_cal))/avg_calorie)*100
    week_cal_perc = ((abs(week_cal))/avg_calorie)*100
    today_res = f"Your percentage of daily healthy cosumption is {str(today_cal_perc)[:6]}%"
    week_res = f"Your average percentage of healthy consumption for past 7 days is {str(week_cal_perc)[:6]}%"
    # print(today_res)
    # print(week_res)
    users = list(set(list(today_overall_df["user_id"])))
    overallsums = []
    overallavg = []
    cols3 = ["allnutrient", "user", "all", "avg"]
    for i in (nutrients2):
        overallsums.append(sum(list(today_overall_df[i])))
        overallavg.append(sum(list(today_overall_df[i]))/len(users))
    # print(overallsums)
    # print(overallavg)
    overall = []
    for i in range(len(nutrients2)):
        overall.append(
            dict(zip(cols3, [nutrients2[i], sums[i], overallsums[i], overallavg[i]])))
    print(overall)
    overall = dumps(overall)
    return render(request, 'purchaseComparison.html', context={'today': nutrients_sum1, 'week': nutrients_sum2, 'today_res': today_res, 'week_res': week_res, 'overall': overall})


def consumeComparison(request):
    url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    user1 = request.user
    user_id = user1.username
    data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body> 
        </soapenv:Envelope>"""

    response = requests.post(url, data=data2, headers=headers)
    # print(response)
    x = response.content.decode('utf-8')
    # print(x)
    z = x.strip().split('Table')
    print(z)
    food_name = []
    date = []
    quantity = []
    calorie = []
    meal_type = []
    time = []

    for i in range(3, len(z)):
        if(i % 3 == 0):
            food_name.append(
                re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
            date.append(
                re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
            quantity.append(
                re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
            calorie.append(
                re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
            meal_type.append(
                re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
            time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

    user_log = pd.DataFrame()
    user_log['food_name'] = food_name
    user_log['date'] = date
    user_log['time'] = time
    user_log['quantity'] = quantity
    user_log['calorie'] = calorie
    user_log['meal_type'] = meal_type
    # print(user_log)

    prev_date = dt.date.today() - dt.timedelta(days=1)
    d4 = dt.date.strftime(prev_date, "%m/%d/%Y")
    today = datetime.strptime(str(dt.date.today()),
                              '%Y-%m-%d').strftime('%m/%d/%Y')
    if(len(calx) > 0):
        del calx[:]
    '''
        for i in range(5):
            prev_date = nd - dt.timedelta(days=i)
            d4 = dt.date.strftime(prev_date, "%m/%d/%Y")
            # print(d4)
        
            listdate.append(d4)
        # print(listdate)
        listof = []
        '''
    nutdata = []
    a = []

    today_df = user_log[user_log.date == today]

    def func(s):
        return int(s)
    today_df['quantity'] = today_df['quantity'].apply(func)
    # print(today_df)
    # print(today_df['food_name'])
    foods = list(set(list(today_df['food_name'])))
    # print(foods)

    food = []
    calorie = []
    carb = []
    fat = []
    alcohol = []
    fiber = []
    sugar = []
    sodium = []
    qnt = []
    for i in foods:
        strin = i
        # print(strin)
        data = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <getFood xmlns="http://tempuri.org/">
                    <name>"""+str(strin)+"""</name>
                    </getFood>
                </soap:Body>
                </soap:Envelope>"""
        r = requests.post(url, data=data, headers=headers)
        response = requests.post(url, data=data, headers=headers)
        x = response.content.decode('utf-8')
        z = x.strip().split('Table')
        a.append(z)
        fdf = sum(list(today_df[today_df['food_name'] == strin]['quantity']))
        qnt.append(fdf)
        for i in range(3, len(z)):
            if(i % 3 == 0):
                food.append(
                    (re.search('<FM_NAME>(.*)</FM_NAME>', z[i]).group(1)))
                carb.append(
                    int(re.search('<FM_CARBOHYDRATE>(.*)</FM_CARBOHYDRATE>', z[i]).group(1)))
                fat.append(
                    int(re.search('<FM_FAT>(.*)</FM_FAT>', z[i]).group(1)))
                fiber.append(
                    int(re.search('<FM_FIBER>(.*)</FM_FIBER>', z[i]).group(1)))
                alcohol.append(
                    int(re.search('<FM_ALCHOHOL>(.*)</FM_ALCHOHOL>', z[i]).group(1)))
                sugar.append(
                    int(re.search('<FM_SUGAR>(.*)</FM_SUGAR>', z[i]).group(1)))
                sodium.append(
                    int(re.search('<FM_SODIUM>(.*)</FM_SODIUM>', z[i]).group(1)))
                calorie.append(
                    int(re.search('<FM_CALORIE>(.*)</FM_CALORIE>', z[i]).group(1)))
                break

    onedaycons = []
    for i in range(len(foods)):
        onedaycons.append({'foodname': foods[i], 'carbs': qnt[i]*carb[i], 'fat': qnt[i]*fat[i], 'sugar': qnt[i]*sugar[i],
                           'fiber': qnt[i]*fiber[i], 'sodium': qnt[i]*sodium[i], 'alcohol': qnt[i]*alcohol[i], 'calorie': qnt[i]*calorie[i]})

    carbsum = []
    fatsum = []
    alcsum = []
    fibsum = []
    sugarsum = []
    sodsum = []
    calsum = []

    for i in onedaycons:
        carbsum.append(i['carbs'])
        fatsum.append(i['fat'])
        alcsum.append(i['alcohol'])
        sugarsum.append(i['sugar'])
        fibsum.append(i['fiber'])
        sodsum.append(i['sodium'])
        calsum.append(i['calorie'])

    # print(onedaycons)
    # print(today_df)
    # print(qnt)

    nutrients = ["carbs", "fat", "fiber",
                 "sodium", "alcohol", "sugar", "calorie"]
    consumed = [sum(carbsum), sum(fatsum), sum(fibsum), sum(
        sodsum), sum(alcsum), sum(sugarsum), sum(calorie)]
    cols = ["nutrient", "quantity"]
    nutrients_consumed = []
    for i in range(len(nutrients)):
        nutrients_consumed.append(dict(zip(cols, [nutrients[i], consumed[i]])))
    nutrients_consumed = dumps(nutrients_consumed)
    print(nutrients_consumed)

    ###########################################################################################
    # LAST WEEK DATA
    todayy = dt.date.today()
    prev_date = todayy - dt.timedelta(days=7)
    # print(prev_date)
    prev_date = datetime.strptime(
        str(prev_date), '%Y-%m-%d').strftime('%m/%d/%Y')
    # print(prev_date)

    week_df = user_log[(user_log.date >= prev_date) & (user_log.date <= today)]
    # print(week_df)
    week_df['quantity'] = week_df['quantity'].apply(func)
    week_food = list(set(list(week_df['food_name'])))
    # print(week_food)
    week_dates = sorted(list(set(list(week_df['date']))))

    day_data = []

    for d in week_dates:
        # print(d)
        food2 = []
        calorie2 = []
        carb2 = []
        fat2 = []
        alcohol2 = []
        fiber2 = []
        sugar2 = []
        sodium2 = []
        qnt2 = []
        for i in week_food:
            strin = i
            # print(strin)
            data = """<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <getFood xmlns="http://tempuri.org/">
                        <name>"""+str(strin)+"""</name>
                        </getFood>
                    </soap:Body>
                    </soap:Envelope>"""
            r = requests.post(url, data=data, headers=headers)
            response = requests.post(url, data=data, headers=headers)
            x = response.content.decode('utf-8')
            z = x.strip().split('Table')
            a.append(z)
            fdf = sum(
                list(week_df[(week_df.food_name == strin) & (week_df.date == d)]['quantity']))
            qnt2.append(fdf)
            for i in range(3, len(z)):
                if(i % 3 == 0):
                    food2.append(
                        (re.search('<FM_NAME>(.*)</FM_NAME>', z[i]).group(1)))
                    carb2.append(
                        int(re.search('<FM_CARBOHYDRATE>(.*)</FM_CARBOHYDRATE>', z[i]).group(1)))
                    fat2.append(
                        int(re.search('<FM_FAT>(.*)</FM_FAT>', z[i]).group(1)))
                    fiber2.append(
                        int(re.search('<FM_FIBER>(.*)</FM_FIBER>', z[i]).group(1)))
                    alcohol2.append(
                        int(re.search('<FM_ALCHOHOL>(.*)</FM_ALCHOHOL>', z[i]).group(1)))
                    sugar2.append(
                        int(re.search('<FM_SUGAR>(.*)</FM_SUGAR>', z[i]).group(1)))
                    sodium2.append(
                        int(re.search('<FM_SODIUM>(.*)</FM_SODIUM>', z[i]).group(1)))
                    calorie2.append(
                        int(re.search('<FM_CALORIE>(.*)</FM_CALORIE>', z[i]).group(1)))
                    break

        onedaycons2 = []
        for i in range(len(week_food)):
            onedaycons2.append({'foodname': week_food[i], 'carbs': qnt2[i]*carb2[i], 'fat': qnt2[i]*fat2[i], 'sugar': qnt2[i]*sugar2[i],
                                'fiber': qnt2[i]*fiber2[i], 'sodium': qnt2[i]*sodium2[i], 'alcohol': qnt2[i]*alcohol2[i], 'calorie': qnt2[i]*calorie2[i]})

        carbsum2 = []
        fatsum2 = []
        alcsum2 = []
        fibsum2 = []
        sugarsum2 = []
        sodsum2 = []
        calsum2 = []
        for i in onedaycons2:
            carbsum2.append(i['carbs'])
            fatsum2.append(i['fat'])
            alcsum2.append(i['alcohol'])
            sugarsum2.append(i['sugar'])
            fibsum2.append(i['fiber'])
            sodsum2.append(i['sodium'])
            calsum2.append(i['calorie'])
        # print(onedaycons)
        # print(today_df)
        # print(qnt)

        nutrients2 = ["carbs", "fat", "fiber",
                      "sodium", "alcohol", "sugar", "calorie"]
        consumed2 = [sum(carbsum2), sum(fatsum2), sum(fibsum2), sum(
            sodsum2), sum(alcsum2), sum(sugarsum2), sum(calsum2)]
        cols2 = ["nutrient", "quantity"]
        nutrients_consumed2 = []
        for i in range(len(nutrients2)):
            nutrients_consumed2.append(
                dict(zip(cols2, [nutrients2[i], consumed2[i]])))
        #nutrients_consumed2 = dumps(nutrients_consumed2)
        # print(nutrients_consumed2)

        day_data.append(nutrients_consumed2)

    #week_data = dumps(week_data)
    # print(day_data)
    week_data = []
    cols3 = ["date", "data"]
    for i in range(len(week_dates)):
        week_data.append(dict(zip(cols3, [week_dates[i], day_data[i]])))

    week_data = dumps(week_data)
    print(week_data)
    # purchaseComparison(request)
    return render(request, 'consumeComparison.html', context={"nutrients": nutrients_consumed, "weekNutrients": week_data})


def cuisine_cards(request):

    return render(request, 'cuisine_cards.html')



def south(request):
    user_id = request.user
    user = user_id.username
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    
    items = Old_Food_Diary.objects.filter(food_type='South Indian Food')
    title = "South Indian"
    consumed = cuisine_consumption_temp.objects.filter(food_type='South Indian Food', user_id=user)
    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
   # context_dict={'north_indian':north_indian,'page':page}
    return render(request, 'assorted.html', {'items': items, 'consumed': consumed, 'date': d2, 'page': page, 'title': title, 'name': name})


def chinese(request):
    user_id = request.user
    user = user_id.username
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    items = Old_Food_Diary.objects.filter(food_type='Chinese')
    title = "Chinese"
    consumed = cuisine_consumption_temp.objects.filter(food_type='Chinese', user_id=user)
    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
   # context_dict={'north_indian':north_indian,'page':page}
    return render(request, 'assorted.html', {'items': items, 'consumed': consumed, 'date': d2, 'page': page, 'title': title, 'name': name})


def continental(request):
    user_id = request.user
    user = user_id.username
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    items = Old_Food_Diary.objects.filter(food_type='Continental')
    title = "Continental"
    consumed = cuisine_consumption_temp.objects.filter(food_type='Continental', user_id=user)
    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
   # context_dict={'north_indian':north_indian,'page':page}
    return render(request, 'assorted.html', {'items': items, 'consumed': consumed, 'date': d2, 'page': page, 'title': title, 'name': name})


def sweet(request):
    user_id = request.user
    user = user_id.username
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    items = Old_Food_Diary.objects.filter(food_type='Sweet Dish')
    title = "Sweet Dish"
    consumed = cuisine_consumption_temp.objects.filter(food_type='Sweet Dish', user_id=user)
    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
   # context_dict={'north_indian':north_indian,'page':page}
    return render(request, 'assorted.html', {'items': items, 'consumed': consumed, 'date': d2, 'page': page, 'title': title, 'name': name})


def confirm_consumption(request):
    if request.method == "POST":
        user_id = request.user
        user = user_id.username
        print(user)
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        f_name = request.POST.get("selectedItem2")
        quantity = request.POST.get("selectedQuant")
        food_id = request.POST.get("f_id")
        print(food_id)
        food_type = request.POST.get("f_type")
        if(food_type == "South Indian"):
            food_type = "South Indian Food"
        meal_type = request.POST.get("meal_type")
        f = Old_Food_Diary.objects.get(food_id=food_id)
        quantity = int(quantity)
        cal = float(f.calories)
        cal = cal*quantity
        fats = float(f.fats)
        fats = fats*quantity
        prot = float(f.protein)
        prot = prot*quantity
        carbs = float(f.carbohydrates)
        carbs = carbs*quantity
        new_entry = cuisine_consumption_temp(
            user_id=user,
            date=date,
            time_rec=time,
            quantity=quantity,
            food_id=food_id,
            food_name=f_name,
            food_type=food_type,
            calories=cal,
            fats=fats,
            protein=prot,
            carbohydrates=carbs,
            meal_type=meal_type,
        )
        new_entry.save()
    if(food_type == "South Indian Food"):
        return redirect('/south')
    elif(food_type == "Chinese"):
        return redirect('/chinese')
    elif(food_type == "Continental"):
        return redirect('/continental')
    elif(food_type == "Sweet Dish"):
        return redirect('/sweet')


def cuisine_consumed(request):
    user_id = request.user
    user = user_id.username
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y %H:%M:%S")
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    try:
        item = cuisine_consumption_temp.objects.filter(user_id=user)
    except cuisine_consumption_temp.DoesNotExist:
        item = None
    return render(request, 'cuisine_consumed.html', {'info': item, 'name': name, 'date_time': d1})


def delete_cuisine(request, c_id):
    try:
        f = cuisine_consumption_temp.objects.get(c_id=c_id)
        food_type = f.food_type
        f.delete()
    except:
        f = None
    if(food_type == "South Indian Food"):
        return redirect('/south')
    elif(food_type == "Chinese"):
        return redirect('/chinese')
    elif(food_type == "Continental"):
        return redirect('/continental')
    elif(food_type == "Sweet Dish"):
        return redirect('/sweet')


def delete_cuisine2(request, c_id):
    try:
        f = cuisine_consumption_temp.objects.get(c_id=c_id)
        food_type = f.food_type
        f.delete()
    except:
        f = None
    return redirect('/cuisine_consumed')


def confirm_file1(request):
    if request.method == "POST":
        user_id = request.user
        user = user_id.username
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        files = request.FILES["upload_file"]
        food_type = request.POST.get("f_type1")
        if(food_type == "South Indian"):
            f_type = "South Indian Food"
        elif(food_type == "Sweet dish"):
            f_type = "Sweet Dish"
        elif(food_type == "Chinese"):
            f_type = "Chinese"
        elif(food_type == "Continental"):
            f_type = "Continental"
        df = pd.read_csv(files, encoding='utf-8')
        if(len(df.columns) != 7):
            return render(request, "error.html")
        new_header = ['f_name', 'cal', 'prot',
                      'fats', 'carbs', 'quantity', 'mealtype']
        df.columns = new_header
        for i in df.iterrows():
            q = int(i[1][5])
            cal = float(i[1][1])
            cal = cal*q
            prot = float(i[1][2])
            prot = prot*q
            carbs = float(i[1][4])
            carbs = carbs*q
            fats = float(i[1][3])
            fats = fats*q
            new_entry = cuisine_consumption_temp(
                user_id=user,
                date=date,
                time_rec=time,
                quantity=i[1][5],
                food_id=0,
                food_name=i[1][0],
                food_type=f_type,
                calories=cal,
                fats=fats,
                protein=prot,
                carbohydrates=carbs,
                meal_type=i[1][6],
            )
            new_entry.save()
        if(f_type == "South Indian Food"):
            return redirect('/south')
        elif(f_type == "Chinese"):
            return redirect('/chinese')
        elif(f_type == "Continental"):
            return redirect('/continental')
        elif(f_type == "Sweet Dish"):
            return redirect('/sweet')


def confirm_file2(request):
    if request.method == "POST":
        user_id = request.user
        user = user_id.username
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        files = request.FILES["upload_file"]
        df = pd.read_csv(files, encoding='utf-8')
        if(len(df.columns) != 8):
            return render(request, "error.html")
        new_header = ['f_name', 'cal', 'prot', 'fats',
                      'carbs', 'quantity', 'mealtype', 'food_type']
        df.columns = new_header
        for i in df.iterrows():
            if(i[1][7] == "South Indian"):
                f_type = "South Indian Food"
            else:
                f_type = i[1][7]
            q = int(i[1][5])
            cal = float(i[1][1])
            cal = cal*q
            prot = float(i[1][2])
            prot = prot*q
            carbs = float(i[1][4])
            carbs = carbs*q
            fats = float(i[1][3])
            fats = fats*q
            new_entry = cuisine_consumption_temp(
                user_id=user,
                date=date,
                time_rec=time,
                quantity=i[1][5],
                food_id=0,
                food_name=i[1][0],
                food_type=f_type,
                calories=cal,
                fats=fats,
                protein=prot,
                carbohydrates=carbs,
                meal_type=i[1][6],
            )
            new_entry.save()
            return redirect('/cuisine_consumed')


def confirm_file3(request):
    if request.method == "POST":
        user_id = request.user
        user = user_id.username
        files = request.FILES["upload_file"]
        shop_name = request.POST.get("f_type1")
        df = pd.read_csv(files, encoding='utf-8')
        if(len(df.columns) != 14):
            return render(request, "error2.html")
        new_header = ['food_name', 'quantity', 'serving style', 'carbs', 'protein', 'fat', 'fiber',
                      'sugar', 'sodium', 'alchohol', 'calorie', 'calorie_saturated_fats', 'shop_name', 'mfg']
        df.columns = new_header
        for i in df.iterrows():
            quantity = int(i[1][1])
            carbs = float(i[1][3])
            carbs = carbs*quantity
            protein = float(i[1][4])
            protein = protein*quantity
            fat = float(i[1][5])
            fat = fat*quantity
            fiber = float(i[1][6])
            fiber = fiber*quantity
            sugar = float(i[1][7])
            sugar = sugar*quantity
            sodium = float(i[1][8])
            sodium = sodium*quantity
            alchohol = float(i[1][9])
            alchohol = alchohol*quantity
            calorie = float(i[1][10])
            calorie = calorie*quantity
            calorie_saturated_fats = float(i[1][11])
            calorie_saturated_fats = calorie_saturated_fats*quantity
            new_entry = Temporary_purchase_new(
                user_id=user_id,
                mfg_code=i[1][13],
                food_name=i[1][0],
                carbs=carbs,
                protein=protein,
                fat=fat,
                fiber=fiber,
                sugar=sugar,
                sodium=sodium,
                calorie=calorie,
                alchohol=alchohol,
                calorie_saturated_fats=calorie_saturated_fats,
                shop_name=i[1][12],
                quantity=i[1][1],
                ss_code=i[1][2],
            )
            new_entry.save()
    if(shop_name == "Others"):
        return redirect('/others')
    else:
        return redirect('/purchase')


def confirm_file4(request):
    if request.method == "POST":
        user_id = request.user
        user = user_id.username
        files = request.FILES["upload_file"]
        shop_name = request.POST.get("f_type1")
        df = pd.read_csv(files, encoding='utf-8')
        if(len(df.columns) != 13):
            return render(request, "error3.html")
        new_header = ['food_name', 'quantity', 'serving style', 'carbs', 'protein', 'fat',
                      'fiber', 'sugar', 'sodium', 'alchohol', 'calorie', 'calorie_saturated_fats', 'mfg']
        df.columns = new_header
        for i in df.iterrows():
            quantity = int(i[1][1])
            carbs = float(i[1][3])
            carbs = carbs*quantity
            protein = float(i[1][4])
            protein = protein*quantity
            fat = float(i[1][5])
            fat = fat*quantity
            fiber = float(i[1][6])
            fiber = fiber*quantity
            sugar = float(i[1][7])
            sugar = sugar*quantity
            sodium = float(i[1][8])
            sodium = sodium*quantity
            alchohol = float(i[1][9])
            alchohol = alchohol*quantity
            calorie = float(i[1][10])
            calorie = calorie*quantity
            calorie_saturated_fats = float(i[1][11])
            calorie_saturated_fats = calorie_saturated_fats*quantity
            new_entry = Temporary_purchase_new(
                user_id=user_id,
                mfg_code=i[1][12],
                food_name=i[1][0],
                carbs=carbs,
                protein=protein,
                fat=fat,
                fiber=fiber,
                sugar=sugar,
                sodium=sodium,
                calorie=calorie,
                alchohol=alchohol,
                calorie_saturated_fats=calorie_saturated_fats,
                shop_name=shop_name,
                quantity=i[1][1],
                ss_code=i[1][2],


            )
            new_entry.save()
    if(shop_name == 'amazon'):
        return redirect('/amazon')
    elif(shop_name == "Bigbasket"):
        return redirect('/bb/')
    elif(shop_name == "Grofers"):
        return redirect('/grofers')


def save_cuisine(request):
    try:
        f = cuisine_consumption_temp.objects.all()
        for i in f:
            new_entry = cuisine_consumption_det(
                user_id=i.user_id,
                date=i.date,
                time_rec=i.time_rec,
                quantity=i.quantity,
                food_id=i.food_id,
                food_name=i.food_name,
                food_type=i.food_type,
                calories=i.calories,
                fats=i.fats,
                protein=i.protein,
                carbohydrates=i.carbohydrates,
                meal_type=i.meal_type,
            )
            new_entry.save()
            i.delete()
    except:
        f = None
    return redirect('/cuisine_consumed')


def confirm_consumption2(request):
    if request.method == "POST":
        user_id = request.user
        user = user_id.username
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        f_name = request.POST.get("selectedItem3")
        quantity = request.POST.get("quantity3")

        f_type = request.POST.get("f_type3")
        print(f_type)
        cal = request.POST.get("cal3")
        prot = request.POST.get("protin3")
        carbs = request.POST.get("carbs3")
        fats = request.POST.get("fat3")
        if(f_type == "South Indian"):
            f_type = "South Indian Food"

        meal_type = request.POST.get("meal_type3")
        quantity = int(quantity)
        cal = float(cal)
        cal = cal*quantity
        fats = float(fats)
        fats = fats*quantity
        prot = float(prot)
        prot = prot*quantity
        carbs = float(carbs)
        carbs = carbs*quantity
        new_entry = cuisine_consumption_temp(
            user_id=user,
            date=date,
            time_rec=time,
            quantity=quantity,
            food_id=0,
            food_name=f_name,
            food_type=f_type,
            calories=cal,
            fats=fats,
            protein=prot,
            carbohydrates=carbs,
            meal_type=meal_type,
        )
        new_entry.save()
    if(f_type == "South Indian Food"):
        return redirect('/south')
    elif(f_type == "Chinese"):
        return redirect('/chinese')
    elif(f_type == "Continental"):
        return redirect('/continental')
    elif(f_type == "Sweet Dish"):
        return redirect('/sweet')


def amazon_search(request):
    amazonquery = request.GET['amazonquery']
    if len(amazonquery) > 100:
        allamazon = purchase_cards.objects.none()
    elif(amazonquery == ''):
        allamazon = purchase_cards.objects.none()
    else:
        allamazon = purchase_cards.objects.filter(
            food_name__icontains=amazonquery, shop_name='amazon')
        print(allamazon)
    if allamazon.count() == 0:
        messages.error(request, "Please fill the correct food item")

    params = {'allamazon': allamazon, 'amazonquery': amazonquery}
    return render(request, 'amazon_search.html', params)




def groffers_search(request):
    groffersquery = request.GET['groffersquery']
    if len(groffersquery) > 100:
        allgroffers = purchase_cards.objects.none()
    elif(groffersquery == ''):
        allgroffers = purchase_cards.objects.none()
    else:
        allgroffers = purchase_cards.objects.filter(
            food_name__icontains=groffersquery, shop_name='Grofers')
        # print(allamazon)
    if allgroffers.count() == 0:
        messages.error(request, "Please fill the correct food item")

    params = {'allgroffers': allgroffers, 'groffersquery': groffersquery}
    return render(request, 'groffers_search.html', params)



def bb_search(request):
    bbquery = request.GET['bbquery']
    if len(bbquery) > 100:
        allbb = purchase_cards.objects.none()
    elif(bbquery == ''):
        allbb = purchase_cards.objects.none()
    else:
        allbb = purchase_cards.objects.filter(
            food_name__icontains=bbquery, shop_name='BigBasket')
        # print(allamazon)
    if allbb.count() == 0:
        messages.error(request, "Please fill the correct food item")

    params = {'allbb': allbb, 'bbquery': bbquery}
    return render(request, 'bb_search.html', params)

def other_search(request):
    otherquery = request.GET['otherquery']
    if len(otherquery) > 100:
        allother = purchase_cards.objects.none()
    elif(otherquery == ''):
        allother = purchase_cards.objects.none()
    else:
        allother = purchase_cards.objects.filter(food_name__icontains=otherquery)
        # print(allamazon)
    if allother.count() == 0:
        messages.error(request, "Please fill the correct food item")

    params = {'allother': allother, 'otherquery': otherquery}
    return render(request, 'other_search.html', params)


def amazon(request):
    user_id = request.user
    user = user_id.username
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    items = purchase_cards.objects.filter(shop_name='amazon')
    purchased = Temporary_purchase_new.objects.filter(shop_name='amazon', user_id=user)
        
    vendor = "amazon"
    paginator = Paginator(items, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
    # context_dict={'amazon_items':amazon_items,'page':page}
    return render(request, 'amazon.html', {'items': items, 'purchased': purchased, 'date': d2,'page': page, 'vendor': vendor})



def grofers(request):
    user_id = request.user
    user = user_id.username
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    items = purchase_cards.objects.filter(shop_name='Grofers')
    purchased = Temporary_purchase_new.objects.filter(shop_name='Grofers', user_id=user)
    vendor = "Grofers"
    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
   # context_dict={'north_indian':north_indian,'page':page}
    return render(request, 'amazon.html', {'items': items, 'purchased': purchased, 'date': d2, 'page': page, 'vendor': vendor})



def bb(request):
    user_id = request.user
    user = user_id.username
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    vendor = "Bigbasket"
    items = purchase_cards.objects.filter(shop_name='BigBasket')
    purchased = Temporary_purchase_new.objects.filter(shop_name='BigBasket', user_id=user)
    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
    return render(request, 'amazon.html', {'items': items, 'purchased': purchased, 'date': d2, 'page': page, 'vendor': vendor})



def others(request):
    user_id = request.user
    user = user_id.username
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    items = purchase_cards.objects.all()
    vendor = "Others"
    exclude_list = ['amazon', 'Bigbasket', 'Grofers']
    purchased = Temporary_purchase_new.objects.exclude(shop_name__in=exclude_list).filter(user_id=user)
    paginator = Paginator(items, 8)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(page.num_pages)
    return render(request, 'amazon.html', {'items': items, 'purchased': purchased, 'date': d2, 'page': page, 'vendor': vendor})






def south_search(request):
    southquery = request.GET['southquery']
    print(southquery)
    if len(southquery) > 100:
        allsouth = Old_Food_Diary.objects.none()
    elif(southquery == ''):
        allsouth = Old_Food_Diary.objects.none()
    else:
        allsouth = Old_Food_Diary.objects.filter(food_name__icontains=southquery,food_type='South Indian Food')
        # print(allamazon)
    if allsouth.count() == 0:
        messages.error(request, "Please fill the correct food item")
    title='South Indian'
    params = {'allsouth': allsouth, 'southquery': southquery,'title':title}
    return render(request, 'south_search.html', params)

def chinese_search(request):
    chinesequery = request.GET['chinesequery']
    if len(chinesequery) > 100:
        allchinese = Old_Food_Diary.objects.none()
    elif(chinesequery == ''):
        allchinese = Old_Food_Diary.objects.none()
    else:
        allchinese = Old_Food_Diary.objects.filter(food_name__icontains=chinesequery,food_type='Chinese')
        # print(allamazon)
    if allchinese.count() == 0:
        messages.error(request, "Please fill the correct food item")

    title='Chinese'
    params = {'allchinese': allchinese, 'chinesequery': chinesequery,'title':title}
    return render(request, 'chinese_search.html', params)


def continental_search(request):
    continentalquery = request.GET['continentalquery']
    if len(continentalquery) > 100:
        allcontinental = Old_Food_Diary.objects.none()
    elif(continentalquery == ''):
        allcontinental = Old_Food_Diary.objects.none()
    else:
        allcontinental = Old_Food_Diary.objects.filter(food_name__icontains=continentalquery,food_type='Continental')
        # print(allamazon)
    if allcontinental.count() == 0:
        messages.error(request, "Please fill the correct food item")
    title='Continental'
    params = {'allcontinental': allcontinental, 'continentalquery': continentalquery,'title':title}
    return render(request, 'continental_search.html', params)



def sweet_search(request):
    sweetquery = request.GET['sweetquery']
    if len(sweetquery) > 100:
        allsweet = Old_Food_Diary.objects.none()
    elif(sweetquery == ''):
        allsweet = Old_Food_Diary.objects.none()
    else:
        allsweet = Old_Food_Diary.objects.filter(food_name__icontains=sweetquery,food_type='Sweet Dish')
        # print(allamazon)
    if allsweet.count() == 0:
        messages.error(request, "Please fill the correct food item")
    title = "Sweet Dish"
    params = {'allsweet': allsweet, 'sweetquery': sweetquery,'title':title}
    return render(request, 'sweet_search.html', params)

def foodtopanadmin(request):
    user_id = request.user
    user = user_id.username
    if request.method == "POST":
        f_name = request.POST.get("foodname")
        desc = request.POST.get("desc")
        #m = request.POST.get("mfg")
        #f_id = request.POST.get("fd_id")
        cal = request.POST.get("cal")
        fat = request.POST.get("fat")
        prot = request.POST.get("protin")
        carbs = request.POST.get("carbs")
        #qnt = request.POST.get("quantity")
        fiber = request.POST.get("fiber")
        sat = request.POST.get("sat")
        sod = request.POST.get("sodium")
        sug = request.POST.get("sugar")
        alc = request.POST.get("alc")
        ss_c = request.POST.get("ss_c")
        sat = request.POST.get("sat")
        #meal = request.POST.get("meal_type")

        print(carbs, fat, prot)

        url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
        headers = {"Content-Type": "text/xml; charset=utf-8"}

        data2 = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <AddFood xmlns="http://tempuri.org/">
            <ME_ID>"""+str(user)+"""</ME_ID>
            <Name>"""+str(f_name)+"""</Name>
            <Description>"""+str(desc)+"""</Description>
            <ss_code>"""+str(ss_c)+"""</ss_code>
            <Protin>"""+str(prot)+"""</Protin>
            <Carbohydrate>"""+str(carbs)+"""</Carbohydrate>
            <Fat>"""+str(fat)+"""</Fat>
            <Fiber>"""+str(fiber)+"""</Fiber>
            <Sugar>"""+str(sug)+"""</Sugar>
            <Sodium>"""+str(sod)+"""</Sodium>
            <Alchohol>"""+str(alc)+"""</Alchohol>
            <Calorie>"""+str(cal)+"""</Calorie>
            <Calorie_saturated_fats>"""+str(sat)+"""</Calorie_saturated_fats>
            </AddFood>
        </soap:Body>
        </soap:Envelope>"""
        print(data2)

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')
        print(z[0])
        if "true" in z[0]:
            messages.success(
                request, f"Food Item:{f_name} added successfully to PAN!!")
        elif "false" in z[0]:
            messages.error(request, f"Can not add food item.")

        return redirect('/foodtopanadmin')
    else:
        return render(request, 'foodtopanadmin.html')


def csvtopanadmin(request):
    user_id = request.user
    user = user_id.username
    if request.method == "POST":
        files = request.FILES["csvfile"]
        df = pd.read_csv(files, encoding='unicode-escape')
        print(df)

        true, false = 0, 0

        for i in range(df.shape[0]):
            user = user
            f_name = df.iloc[i]['f_name']
            desc = df.iloc[i]['desc']
            ss_c = df.iloc[i]['ss_c']
            cal = df.iloc[i]['cal']
            fat = df.iloc[i]['fat']
            prot = df.iloc[i]['prot']
            carbs = df.iloc[i]['carbs']
            alc = df.iloc[i]['alc']
            sat = df.iloc[i]['sat']
            fiber = df.iloc[i]['fiber']
            sod = df.iloc[i]['sod']
            sug = df.iloc[i]['sug']

            function_for_batch_upload(user=user, f_name=f_name, desc=desc, ss_c=ss_c, cal=cal, fat=fat, prot=prot, carbs=carbs, alc=alc, sat=sat, fiber=fiber, sod=sod, sug=sug)
            if function_for_batch_upload(user=user, f_name=f_name, desc=desc, ss_c=ss_c, cal=cal, fat=fat, prot=prot, carbs=carbs, alc=alc, sat=sat, fiber=fiber, sod=sod, sug=sug):
                true += 1
            else:
                false += 1

        messages.info(request, f"Total Items In File:{df.shape[0]}; #Food Items Successfully Added:{true}; #Food Items Failed To Add:{false}")
            

        return redirect('/csvtopanadmin')
    else:
        return render(request, 'csvtopanadmin.html')


def csvtopanadminloader(request):
    return render(request, 'csvtopanadmin.html')

def function_for_batch_upload(user, f_name, desc, ss_c, cal, fat, prot, carbs, alc, sat, fiber, sod, sug):
        url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
        headers = {"Content-Type": "text/xml; charset=utf-8"}

        data2 = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <AddFood xmlns="http://tempuri.org/">
            <ME_ID>"""+str(user)+"""</ME_ID>
            <Name>"""+str(f_name)+"""</Name>
            <Description>"""+str(desc)+"""</Description>
            <ss_code>"""+str(ss_c)+"""</ss_code>
            <Protin>"""+str(prot)+"""</Protin>
            <Carbohydrate>"""+str(carbs)+"""</Carbohydrate>
            <Fat>"""+str(fat)+"""</Fat>
            <Fiber>"""+str(fiber)+"""</Fiber>
            <Sugar>"""+str(sug)+"""</Sugar>
            <Sodium>"""+str(sod)+"""</Sodium>
            <Alchohol>"""+str(alc)+"""</Alchohol>
            <Calorie>"""+str(cal)+"""</Calorie>
            <Calorie_saturated_fats>"""+str(sat)+"""</Calorie_saturated_fats>
            </AddFood>
        </soap:Body>
        </soap:Envelope>"""
        print(data2)

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')
        print(z[0])
        if "true" in z[0]:
            print("True")
            return True
        elif "false" in z[0]:
            print("False")
            return False

def consumption_cuisine_status(request):
    if request.method=="POST":
        select_from=request.POST['fromdate']
        select_to=request.POST['todate']
        user1 = request.user
        user_id = user1.username
        combine_date_cuisine=cuisine_consumption_det.objects.filter(user_id=user_id,date__range=[select_from, select_to]).order_by('date')
        con={'combine_date_cuisine':combine_date_cuisine}
        return render(request,'consumption_cuisine_status.html',con)

    else:
        user1 = request.user
        user_id = user1.username
        
        print(user_id)
        print(date.today())
        dates=date.today()
        all_objects = cuisine_consumption_det.objects.filter(user_id=user_id,date=dates).order_by('-date')
        print(all_objects)
        
        con = {'all_objects': all_objects,}
        return render(request, 'consumption_cuisine_status.html', con)