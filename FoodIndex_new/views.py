from json import dumps
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from FoodIndex_new.models import *
from home_app_new.models import *
from basic_app_new.models import *
import requests
import pandas as pd
import csv
from sqlalchemy import create_engine
import mysql.connector as msql
import openpyxl
import pymysql
import numpy as np
from basic_app_new.update import *
import xml.etree.ElementTree as ET
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as lg
# Create your views here.


def upload_csv(request):
    if request.method == "POST":
        mail = request.POST['mail']
        pwd = request.POST['pass']
        #engine = create_engine("mysql+pymysql://{user}:{password}@15.207.8.17/{db}".format(user="Food", password="zhTnxpRFiSzpaF2J", db="Food"))

        mydb = msql.connect(host="15.207.8.17", user="Food",
                            password="zhTnxpRFiSzpaF2J", db="Food")
        table = "SELECT*FROM admin_data"
        df = pd.read_sql(table, mydb)
        mails = list(df['Email_ID'])
        pwds = list(df['Password'])
        admins = dict(zip(mails, pwds))
        if mail not in mails:
            messages.error(
                request, "Email not registered as ADMIN. Use an Email registered as ADMIN.")
            return redirect("/alreadyuser")
        else:
            if admins[mail] == pwd:
                return render(request, 'upload_file.html')
            else:
                messages.error(request, "Incorrect Password.")
                return redirect("/alreadyuser")


def file_to_db(request):
    if request.method == "POST":
        # READING THE INPUT CSV FILE FROM DATABASE
        try:
            files = request.FILES["filename"]
            df = pd.read_csv(files, encoding='unicode-escape')

            myconn = msql.connect(host="15.207.8.17",
                                user="Food", password="zhTnxpRFiSzpaF2J")
            concursor = myconn.cursor()
            concursor.execute("CREATE DATABASE IF NOT exists Food")
            mydb = msql.connect(host="15.207.8.17", user="Food",
                                password="zhTnxpRFiSzpaF2J", db="Food")
            cursor = mydb.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS basic_app_new_old_food_diary(mfg_code VARCHAR(10), food_id VARCHAR(10), food_name VARCHAR(50), description VARCHAR(200), food_type VARCHAR(200), calories VARCHAR(10),fats VARCHAR(10), protein VARCHAR(10), carbohydrates VARCHAR(10), link_of_image VARCHAR(1000), link_of_recipie VARCHAR(1000), purchasing_link VARCHAR(1000))")
            engine = create_engine("mysql+pymysql://{user}:{password}@15.207.8.17/{db}".format(
                user="Food", password="zhTnxpRFiSzpaF2J", db="Food"))

            df.to_sql("basic_app_new_old_food_diary", con=engine,
                    if_exists='append', chunksize=1000, index=False)

            messages.success(request, "File Uploaded Successfully.")
            return redirect("/upload_csv_")
        except:
            messages.error(request, "Duplicates found in the file. Please check the file")
            return redirect("/upload_csv_")
    return redirect("/upload_csv_")


def getdata(request):
    if request.method == 'POST':
        mfgcode = request.POST['mfgcode']
        food_id = request.POST['foodid']
        food_name = request.POST['foodname']
        description = request.POST['description']
        food_type = request.POST['foodtype']
        cal = request.POST['cal']
        protein = request.POST['protein']
        fats = request.POST['fats']
        carbs = request.POST['carbs']
        img = request.POST['img']
        link_of_recipie = request.POST['recipe']
        buy = request.POST['buy']

        myconn = msql.connect(host="15.207.8.17",
                              user="Food", password="zhTnxpRFiSzpaF2J")
        concursor = myconn.cursor()
        concursor.execute("CREATE DATABASE IF NOT exists Food")
        mydb = msql.connect(host="15.207.8.17", user="Food",
                            password="zhTnxpRFiSzpaF2J", db="Food")
        cursor = mydb.cursor()
        table = '''SELECT*FROM basic_app_new_old_food_diary'''
        df = pd.read_sql(table, mydb)

        unique_ids = list(df['food_id'])
        unique_names = list(df['food_name'])

        if (food_id in unique_ids):
            messages.warning(
                request, f"Unable to add the food item. Food ID: {food_id} already present.")
            return redirect("/addfood")

        else:
            cursor.execute("CREATE TABLE IF NOT EXISTS basic_app_new_old_food_diary(mfg_code VARCHAR(10), food_id VARCHAR(10), food_name VARCHAR(50), description VARCHAR(200), food_type VARCHAR(200), calories VARCHAR(10),fats VARCHAR(10), protein VARCHAR(10), carbohydrates VARCHAR(10), link_of_image VARCHAR(1000), link_of_recipie VARCHAR(1000), purchasing_link VARCHAR(1000))")
            query = "INSERT INTO basic_app_new_old_food_diary(mfg_code, food_id, food_name, description, food_type, calories,fats, protein, carbohydrates, link_of_image, link_of_recipie, purchasing_link) VALUES (%s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s, %s)"
            vals = (mfgcode, food_id, food_name, description, food_type,
                    cal, fats, protein, carbs, img, link_of_recipie, buy)
            # mydb.close()
            cursor.execute(query, vals)
            mydb.commit()
            messages.success(
                request, f"New Food '{food_name}' Added To The Table.")
            return redirect("/addfood")


def addfood(request):
    return render(request, 'add_food.html')


def login(request):
    if request.method == "POST":
        admin_nm = request.POST['admin_nm']
        admin_id = request.POST['admin_id']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        repass = request.POST['repass']

        myconn = msql.connect(host="15.207.8.17",
                              user="Food", password="zhTnxpRFiSzpaF2J")
        concursor = myconn.cursor()
        concursor.execute("CREATE DATABASE IF NOT exists Food")
        mydb = msql.connect(host="15.207.8.17", user="Food",
                            password="zhTnxpRFiSzpaF2J", db="Food")
        cursor = mydb.cursor()

        #print(admin_nm, admin_id, phone, email, password, repass)

        if password == repass:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS admin_data(Admin_Name VARCHAR(10), Admin_ID VARCHAR(10), PhoneNo VARCHAR(15), Email_ID VARCHAR(50), Password VARCHAR(20))")

            table = ''' SELECT*FROM admin_data'''
            db = pd.read_sql(table, mydb)
            unique_mail = np.array(db['Email_ID'])
            unique_phn = np.array(db['PhoneNo'])
            unique_id = np.array(db['Admin_ID'])
            unique_name = np.array(db['Admin_Name'])

            if (email in unique_mail) or (admin_id in unique_id) or (admin_nm in unique_name) or (phone in unique_phn):
                messages.info(request, "Admin Already Registered.")
                return redirect("/admin_signup")
            else:
                query = "INSERT INTO admin_data(Admin_Name, Admin_ID, PhoneNo, Email_ID, Password) VALUES (%s, %s, %s, %s, %s)"
                vals = (admin_nm, admin_id, phone, email, password)
                # mydb.close()
                cursor.execute(query, vals)
                mydb.commit()
                return render(request, 'login.html')
        else:
            messages.error(request, "Enter Same Passwords.")
            return redirect("/admin_signup")


def admin_page(request):
    return render(request, 'admin_login.html')


def admin_login(request):
    if request.method == "POST":
        admin = request.POST.get('admin')
        pwd = request.POST.get('pwd')
        
        if (admin=="Z00000000015") and (pwd=="pass"):
            user_id = authenticate(username=admin,password=pwd)
            lg(request,user_id)
            return redirect('/base_table')
        else:
            messages.error(request, "Invalid Admin or Password")
            return render(request, 'admin_login.html')



def abc(request):
    return render(request, 'login.html')


def base_table(request):
    mydb = msql.connect(host="15.207.8.17", user="Food",
                        password="zhTnxpRFiSzpaF2J", db="Food")
    cursor = mydb.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS basic_app_new_old_food_diary(mfg_code VARCHAR(10), food_id VARCHAR(10), food_name VARCHAR(50), description VARCHAR(200), food_type VARCHAR(200), calories VARCHAR(10),fats VARCHAR(10), protein VARCHAR(10), carbohydrates VARCHAR(10), link_of_image VARCHAR(1000), link_of_recipie VARCHAR(1000), purchasing_link VARCHAR(1000))")
    table = ''' SELECT*FROM basic_app_new_old_food_diary'''

    db = pd.read_sql(table, mydb)
    # print(db.columns)
    alldata = []
    for i in range(db.shape[0]):
        temp = db.iloc[i]
        alldata.append(dict(temp))
    context = {"data": alldata}
    #context = dumps(context)
    #print(context)
    return render(request, 'fm_table.html', context)


def xyz(request):
    return render(request, 'upload_file.html')


def user_signup(request):
    return render(request, 'sign-up form.html')


def user_login(request):
    return render(request, 'user_login.html')


def delete_food(request, food_id):
    food_id = str(food_id)
    food = Old_Food_Diary.objects.get(food_id=food_id)
    food.delete()
    return redirect("/base_table")


def update_food(request, food_id):
    food =Old_Food_Diary.objects.get(food_id=food_id)
    print(food)
    updatefood = UpdateFood(request.POST or None, instance=food)
    if updatefood.is_valid():
        updatefood.save()
        return redirect('/base_table')
    return render(request, 'update_form.html', {'update_form': updatefood})


def first_page(request):
    return render(request, 'admin_or_user.html')


def delete_table(request):
    table = Food_diary_new.objects.all()
    table.delete()
    return redirect("/base_table")


def user_signup(request):
    return render(request, "sign-up form.html")


def createnewuser(request):
    if request.method == "POST":
        url = "http://tpancare.panhealth.com/panwebservicev1/Service.asmx?WSDL"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        gender = request.POST.get("gen")
        age = request.POST.get("age")

        x = name.split()
        Firstname = ""
        Midname = ""
        Lastname = ""
        space_count = len(x)
        if(space_count == 1):
            Firstname = x[0]
            Midname = ""
            Lastname = ""
        elif(space_count == 2):
            Firstname = x[0]
            Midname = x[1]
            Lastname = ""
        elif(space_count == 3):
            Firstname = x[0]
            Midname = x[1]
            Lastname = x[2]
        else:
            Firstname = x[0]
            Midname = x[1]
            Lastname = x[2]

        if gender.lower() == "male":
            gender = "m"
        if gender.lower() == "female":
            gender = "f"
        if len(gender) > 1:
            gender = gender[0].upper()
            gender = gender.upper()
        print(Firstname, Midname, Lastname, gender, space_count)

        data = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <CreateNewMember xmlns="http://tempuri.org/">
                            <strFirst>"""+str(Firstname)+"""</strFirst>
                            <strMid>"""+str(Midname)+"""</strMid>
                            <strLast>"""+str(Lastname)+"""</strLast>
                            <strGen>"""+str(gender)+"""</strGen>
                            <strEmailAdd>"""+str(Firstname)+"""@panhealthmail.com</strEmailAdd>
                            <strPhone>"""+str(phone)+"""</strPhone>
                            <intcontacttype>1</intcontacttype>
                        </CreateNewMember>
                    </soap:Body>
                </soap:Envelope>"""

        response = requests.post(url, data=data, headers=headers)
        # print(response)
        xmltree = response.content
        # print(xmltree)
        xmltree = xmltree.decode('utf-8')
        # print(xmltree)
        xmltree = xmltree.strip()
        # print(xmltree)
        myroot = ET.fromstring(xmltree)
        # print(myroot)
        logindetails = []
        # print(logindetails)
        for x in myroot[0][0][0]:
            logindetails.append(x.text)
        # print(logindetails)
        result = "That’s it! You have successfully registered with PanHealth. Your login ID is " + \
            str(logindetails[0])+" and password is "+str(logindetails[1])
        # print(speak_output)
        messages.success(request, result)
        return redirect("/user_signup")
    else:
        return render(request, "sign-up form.html")
def admin_login_purchase(request):
    if request.method == "POST":
        admin = request.POST.get('admin')
        pwd = request.POST.get('pwd')
        if (admin=="Z00000000015") and (pwd=="pass"):
            print(admin, pwd)
            return redirect('/purchase_table')
        else:
            messages.error(request, "Invalid Admin or Password")
            return render(request, 'admin_login.html')

def purchase_table(request):
    mydb = msql.connect(host="15.207.8.17", user="Food",
                        password="zhTnxpRFiSzpaF2J", db="Food")
    cursor = mydb.cursor()
    table = ''' SELECT*FROM basic_app_new_purchase_cards'''
    

    df = pd.read_sql(table, mydb)
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'dataframe': data}
    return render(request, 'purchase_table_admin.html', context)
def admin_login_consumption(request):
    if request.method == "POST":
        admin = request.POST.get('admin')
        pwd = request.POST.get('pwd')
        if (admin=="Z00000000015") and (pwd=="pass"):
            print(admin, pwd)
            return redirect('/consumption_table')
        else:
            messages.error(request, "Invalid Admin or Password")
            return render(request, 'admin_login.html')

def consumption_table(request):
    mydb = msql.connect(host="15.207.8.17", user="Food",
                        password="zhTnxpRFiSzpaF2J", db="Food")
    cursor = mydb.cursor()
    table = ''' SELECT*FROM basic_app_new_food_diary_new'''
    

    df = pd.read_sql(table, mydb)
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'dataframe': data}
    return render(request, 'consumption_table_admin.html', context)

def delete_purchase_food(request, id):
    #food_id = id
    id = int(id) 
    food = purchase_cards.objects.get(id=id)
    print(food)
    food.delete()
    return redirect("/purchase_table")


def update_purchase_food(request, id):
    food=purchase_cards.objects.get(id=id)
    #print(food)
    updatefood = UpdatePurchaseFood(request.POST or None, instance=food)
    if updatefood.is_valid():
        updatefood.save()
        return redirect('/purchase_table')
    return render(request, 'update_purchase_form.html', {'update_form': updatefood})

def addpurchasefood(request):
    if request.method == 'POST':
        food_name = request.POST['foodname']
        description = request.POST['description']
        ss_type = request.POST['sstype']
        cal = request.POST['cal']
        protein = request.POST['protein']
        fats = request.POST['fats']
        carbs = request.POST['carbs']
        img = request.POST['img']

        myconn = msql.connect(host="15.207.8.17",
                              user="Food", password="zhTnxpRFiSzpaF2J")
        concursor = myconn.cursor()
        concursor.execute("CREATE DATABASE IF NOT exists Food")
        mydb = msql.connect(host="15.207.8.17", user="Food",
                            password="zhTnxpRFiSzpaF2J", db="Food")
        cursor = mydb.cursor()
        table = '''SELECT*FROM basic_app_new_purchase_cards'''
        df = pd.read_sql(table, mydb)

        #cursor.execute("CREATE TABLE IF NOT EXISTS basic_app_new_old_food_diary(mfg_code VARCHAR(10), food_id VARCHAR(10), food_name VARCHAR(50), description VARCHAR(200), food_type VARCHAR(200), calories VARCHAR(10),fats VARCHAR(10), protein VARCHAR(10), carbohydrates VARCHAR(10), link_of_image VARCHAR(1000), link_of_recipie VARCHAR(1000), purchasing_link VARCHAR(1000))")
        query = "INSERT INTO basic_app_new_purchase_cards(food_name, description, ss_code, calorie, fat, protein, carbs, image_path) VALUES (%s, %s, %s, %s, %s, %s ,%s, %s)"
        vals = (food_name, description, ss_type, cal, fats, protein, carbs, img)
        # mydb.close()
        cursor.execute(query, vals)
        mydb.commit()
        messages.success(
                request, f"New Food '{food_name}' Added To The Table.")
        return redirect("/add_purchase_food")
    else:
        return render(request, 'addpurchasefood.html')



