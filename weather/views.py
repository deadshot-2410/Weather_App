from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    err_msg=''
    message=''
    message_class=''
    url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=537c9fc43ecfc70388f24f90da60f4e3'   
    city= 'Belgaum'

    if request.method=='POST':
         form=CityForm(request.POST)

         if form.is_valid():
             new_city=form.cleaned_data['name'].capitalize()
             city_count=City.objects.filter(name=new_city).count()
             if city_count==0:
                 r=requests.get(url.format(new_city)).json()
                 if r['cod']==200:
                     form.save()
                 else:
                     err_msg='City does not exist'
             else:
                 err_msg='City is already there!' 
             

    if err_msg:
        message=err_msg
        message_class='is-danger'
    else:
        message='City added'
        message_class='is-success'
    
    form =CityForm()
    weather_data=[]
    cities=City.objects.all()

    for city in cities:
            

        r=  requests.get(url.format(city)).json()

        city_weather={
            'city': city.name ,
            'temperature': r['main']['temp']  ,
            'description': r['weather'][0]['description']  ,
            'icon': r['weather'][0]['icon']  ,
            'feels_like':r['main']['feels_like']
        }

        weather_data.append(city_weather)

    context={'weather_data':weather_data,
                'form':form,
                'message_class':message_class,
                'message':message}

    return render(request, 'weather/weather.html',context)

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')