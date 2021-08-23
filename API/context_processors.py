from basic_app_new.models import *


def notify(request):
    user = request.session.get('user', None)
    items_left = Temporary_new.objects.filter(user_id = user).count()  
    purchase_left = Temporary_purchase_new.objects.filter(user_id = user).count()          
    assorted_left = cuisine_consumption_temp.objects.filter(user_id = user).count()        
    return {'items_left': items_left,'purchase_left':purchase_left,'assorted_left':assorted_left}