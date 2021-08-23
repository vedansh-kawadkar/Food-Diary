from django.urls import path,include
from home_app_new import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
app_name='home_app_new'


urlpatterns=[
	path('home/',views.home,name='home'),
	#path('renderhome/',views.renderhome, name='renderhome'),
	path('details/<str:f_name>/', views.details, name='details'),
    path('add_item1/', views.add_item1, name='add_item1'),
	path('delete/<str:f_name>/', views.delete, name='delete'),
	path('delete_purchase/<str:f_id>/', views.delete_purchase, name='delete_purchase'),
	path('delete_purchase2/<str:f_id>/', views.delete_purchase2, name='delete_purchase2'),
	path('table/', views.table, name='table'),
	path('purchase/', views.purchase, name='purchase'),
	path('confirm_purchase/', views.confirm_purchase, name='confirm_purchase'),
	path('other_purchase/', views.other_purchase, name='other_purchase'),
	path('confirm_purchase2/', views.confirm_purchase2, name='confirm_purchase2'),
	path('save_table/', views.save_table, name='save_table'),
	path('save_purchase/', views.save_purchase, name='save_purchase'),
	path('deletetemp/',views.deletetemp, name='deletetemp'),
	
	path('foodtopan',views.foodtopan,name='foodtopan'),
    path('profile_page/',views.profile_page,name='profile_page'),
	path('nut/', views.HomeView.as_view(),name='nut'),
    path('api', views.ChartData.as_view(),name='api'),
    path('chartof',views.chartof,name='chartof'),
	path('purchase_status',views.purchase_status,name='purchase_status'),
	path('consumer_history',views.consumer_history,name='consumed_history'),
	path('purchasechart', views.purchasechart, name='purchasechart'),
	path('otherdayanalysis', views.otherdayanalysis, name='otherdayanalysis'),
	path('consumeComparison', views.consumeComparison, name='consumeComparison'),
	path('purchaseComparison', views.purchaseComparison, name='purchaseComparison'),
	path('cuisine_cards/',views.cuisine_cards,name='cuisine_cards'),
	path('south/',views.south,name='south'),
	path('chinese/',views.chinese,name='chinese'),
	path('continental/',views.continental,name='continental'),
	path('sweet/',views.sweet,name='sweet'),
	path('confirm_consumption/',views.confirm_consumption,name='confirm_consumption'),
	path('confirm_consumption2/',views.confirm_consumption2,name='confirm_consumption2'),
	path('cuisine_consumed/',views.cuisine_consumed,name='cuisine_consumed'),
	path('delete_cuisine/<str:c_id>/',views.delete_cuisine,name='delete_cuisine'),
	path('delete_cuisine2/<str:c_id>/',views.delete_cuisine2,name='delete_cuisine2'),
	path('confirm_file1/',views.confirm_file1,name='confirm_file1'),
	path('confirm_file2/',views.confirm_file2,name='confirm_file2'),
	path('confirm_file3/',views.confirm_file3,name='confirm_file3'),
	path('confirm_file4/',views.confirm_file4,name='confirm_file4'),
	path('save_cuisine/',views.save_cuisine,name='save_cuisine'),
	path('amazon/',views.amazon,name='amazon'),
	path('grofers/',views.grofers,name='grofers'),
	path('bb/',views.bb,name='bb'),
	path('others/',views.others,name='others'),
	path('amazon_search/',views.amazon_search,name='amazon_search'),
	path('bb_search/',views.bb_search,name='bb_search'),
	path('other_search/',views.other_search,name='other_search'),
	path('groffers_search/',views.groffers_search,name='groffers_search'),
	path('south_search/',views.south_search,name='south_search'),
	path('continental_search/',views.continental_search,name='continental_search'),
	path('sweet_search/',views.sweet_search,name='sweet_search'),
	path('chinese_search/',views.chinese_search,name='chinese_search'),
	path('foodtopanadmin',views.foodtopanadmin,name='foodtopanadmin'),
	path('consumption_cuisine_status',views.consumption_cuisine_status,name='consumption_cuisine_status'),





]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)