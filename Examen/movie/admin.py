from django.contrib import admin


from .models import Movie
# Register your models here.


class MovieModelAdmin(admin.ModelAdmin):
    fields =[
        'name',
        'slug',
        'studio',
        'year',
        'genre',
        'active',
        'created',
        'updated',
        'get_age',
    ]
    readonly_fields =['created','updated','slug','get_age']

    def get_age(self, obj, *args, **kwargs):
        return str(obj.age)

    class Meta:
        model = Movie

admin.site.register(Movie, MovieModelAdmin)
