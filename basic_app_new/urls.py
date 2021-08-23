from django.urls import path,include
from basic_app_new.views import * 
from django.conf import settings
from django.conf.urls import url
app_name = 'basic_app_new'

urlpatterns=[
   path('north/',north,name='north'),
   path('search',search,name='search'),
   path('purchase/',purchase_card,name='purchase_cards'),
   path('api/purchase_cards',purchase_cards_views.as_view()),
   path('api/cuisine_fooditems',cuisine_fooditems_views.as_view()),
   path('api/purchase_transaction',purchase_transactions_views.as_view()),
   path('api/purchase_food_detail',purchase_fooditem_views.as_view()),
   path('api/cuisine_transaction',cuisine_transactions_views.as_view()),
   path('api/cuisine_food_detail',cuisine_fooditem_views.as_view()),

]
