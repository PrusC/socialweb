from django.shortcuts import render
import requests


def get_weather(request, city):
    api_key = "27feb82c651f14dae80121d7b4bac614"
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city, api_key)

    res = requests.get(url).json()
    print(res)
    city_info = {
        'city': city,
        'temp': res['main']['temp'],
        'icon': res['weather'][0]['icon'],
    }
    context = {
        'info': city_info
    }
    return context

