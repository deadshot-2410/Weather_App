from . import views
from django.urls import path,include

urlpatterns=[
    path('',views.index,name='home'),
    path('delete/<city_name>/',views.delete_city,name='delete_city'),
]