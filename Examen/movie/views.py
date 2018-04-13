from django.shortcuts import render, redirect
import redis, ast, json
from .models import Movie

# Create your views here.
def sql_to_redis(request):
    red = redis.Redis(host='localhost', port=9090, db=0)
    structure = {
        "Movies" : { }
    }
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
    red.hmset("FakeDB", structure)
    return redirect()
