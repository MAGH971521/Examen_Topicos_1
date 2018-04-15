from django.shortcuts import render, redirect
from django.contrib import messages
import redis, ast, json
from .models import Movie

# Create your views here.


def home(request, **kwargs):
    data = None
    for message in messages.get_messages(request):
        data = message
        break
    return render(request, "index.html", context={'values': data})

def sql_to_redis(request):
    red = redis.Redis(host='localhost', port=9090, db=0)
    structure = {
        "Movies" : { }
    }
    data_value = [] 
    for val in list(Movie.objects.all()):
        structure["Movies"].update({
        val.id : {
            "name": val.name,
            "year": val.year,
            "studio": val.studio,
            "genre": val.genre,
            "active": val.active,
            "created": val.created
        }})
        red.sadd("MyDB:Movies:{}".format(val.id), structure["Movies"][val.id])
        data_origin = list(red.smembers("MyDB:Movies:{}".format(val.id)))
        data_value.append(data_origin[0].decode('utf-8'))
    print(data_value)
    message = str(data_value)
    messages.add_message(request, messages.INFO, message)
    return redirect('/')
