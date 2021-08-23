from django.contrib import admin
from django.urls import path, include
from FoodIndex_new import views
from FoodIndex_new.views import *
from django.conf.urls.static import static
from django.conf import settings
from home_app_new import views as hviews
from basic_app_new import views as bviews
app_name='FoodIndex_new'
urlpatterns = [
    path('upload_csv', views.upload_csv, name='upload_csv'),    
    path('filetodb', views.file_to_db, name='filetodb'),
    path('addfood', views.addfood, name='addfood'),
    path('getdata', views.getdata, name='getdata'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_page', views.admin_page, name='admin_page'),
    path('alreadyuser', views.abc, name='alreadyuser'),
    path('base_table', views.base_table, name='base_table'),
    path('upload_csv_', views.xyz, name='upload_csv_'),
    path('user_signup', views.user_signup, name='user_signup'),
    path('user_signup_', views.createnewuser, name='user_signup'),
    path('home', hviews.home, name='home'),
    path('north', bviews.north, name='north'),
    path('table', hviews.table, name='table'),
    path('purchase', hviews.purchase, name='purchase'),
    path('', views.user_login, name='user_login'),
    path('profile_page',hviews.profile_page,name='profile_page'),
    path('search',bviews.search,name='search'),
    path('delete/<str:food_id>',views.delete_food,name="delete"),
    #path('chart',hviews.chart,name='chart'),
	#path('calchartthree',hviews.calchartthree,name='calchartthree'),
    path('update/<str:food_id>', views.update_food, name='update'),
    path('delete_table', views.delete_table, name='delete_table'),
    path('home/userfoodlogchart', hviews.userfoodlogchart, name='userfoodlogchart'),
    path('nut/', hviews.HomeView.as_view(),name='nut'),
    path('api', hviews.ChartData.as_view(),name='api'),
    path('chartof',hviews.chartof,name='chartof'),
    path('bb/',hviews.bb,name='bb'),
    path('amazon/',hviews.amazon,name='amazon'),
    path('grofers/',hviews.grofers,name='grofers'),
    path('south/',hviews.south,name='south'),
    path('chinese/',hviews.chinese,name='chinese'),
	path('continental/',hviews.continental,name='continental'),
	path('sweet/',hviews.sweet,name='sweet'),
    path('others/',hviews.others,name='others'),
    path('cuisine_consumed/',hviews.cuisine_consumed,name='cuisine_consumed'),
    path('purchase_table', views.purchase_table, name='purchase_table'),
    path('admin_login_purchase', views.admin_login_purchase, name='admin_login_purchase'),
    path('consumption_table', views.consumption_table, name='consumption_table'),
    path('admin_login_consumption', views.admin_login_consumption, name='admin_login_consumption'),
    path('delete_purchase/<str:id>',views.delete_purchase_food,name="delete"),
    path('update_purchase/<str:id>', views.update_purchase_food, name='update'),
    path('delete_table', views.delete_table, name='delete_table'),
    path('add_purchase_food', views.addpurchasefood, name='add_purchase_food'),
	path('foodtopanadmin',hviews.foodtopanadmin,name='foodtopanadmin'),
	path('csvtopanadmin',hviews.csvtopanadmin,name='csvtopanadmin'),
	path('csvtopanadmin_',hviews.csvtopanadminloader,name='csvtopanadmin_'),




    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)

