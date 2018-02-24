from datetime import timedelta, datetime, date
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.utils.encoding import smart_text


from .validators import validate_yearfilms, validate_studioname
# Create your models here.

GENRE_CHOICES = (
    ('action','Action'),
    ('comedy','Comedy'),
    ('romance','Romance'),
    ('fantasy','Fantasy'),
    ('horror', 'Horror'),
    ('drama','Drama'),
    ('adventure','Adventure'),
)


class MovieModelQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active = True)

    def returns_namefield(self, value):
        return self.filter(name__icontains = value)

class MovieModelManager(models.Manager):
    def get_queryset(self):
        return MovieModelQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        query_values = super(MovieModelManager, self).all(*args, **kwargs).filter(active=True)
        return query_values


class Movie(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name='Movie\'s name')
    year = models.CharField(max_length=120, blank=True, verbose_name='Movie\s year film', validators=[validate_yearfilms])
    studio = models.CharField(max_length=120, blank=True, verbose_name='Studio\s name', validators=[validate_studioname])
    genre = models.CharField(max_length=120, choices=GENRE_CHOICES, default='action')
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True, verbose_name='Is in the Cinema?')
    created = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now, verbose_name='Registration date')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated Time')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = MovieModelManager()

    def __str__(self):
        return smart_text(str(self.name + ' - ' + self.studio))

    #Metodo encargado de crear urls mas "dinamicas"
    def save(self, *args, **kwargs):
        print("Execute Save method")
        if not self.slug:
            if self.name:
                self.slug = slugify(self.name)
        super(Movie, self).save(*args, **kwargs)

    @property
    def age(self):
        if int(self.year) <= datetime.now().year:
            age_time = datetime.combine(self.created, self.updated.time())
            print(age_time)
            try:
                difference = datetime.now() - age_time
                print(difference)
            except:
                print("Error")
                return "Well... i'm dissapointed :/ "
            if difference <= timedelta(minutes=10):
                print(difference)
                return "Just now!"
            print(timesince(age_time).split(', ')[0])
            return 'Register occurs {time} ago'.format(time=timesince(age_time).split(', ')[0])
        return str("Well... i'm dissapointed again :(")


#Metodos Post y Pre Save
def movie_model_pre_save_receiver(sender, instance, *args, **kwargs):
    print("Execute the method \"movie_model_pre_save_receiver\"")
    if not instance.slug and instance.name:
        instance.slug = slugify(instance.name)
        instance.save()

def movie_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    print("Execute the method \"movie_model_post_save_receiver\"")
    if not instance.slug and instance.name:
        instance.slug = slugify(instance.name)
        instance.save()

pre_save.connect(movie_model_pre_save_receiver, sender=Movie)
post_save.connect(movie_model_post_save_receiver, sender=Movie)
