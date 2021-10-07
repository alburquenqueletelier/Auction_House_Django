from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ModelForm, SelectDateWidget, TextInput
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pass

class auctions(models.Model):
    SPORT = 1
    ELECTRONIC = 2
    HOMELIKE = 3
    FOOD = 4
    CARS = 5

    CAT_TYPE = (
        (SPORT, _('Sport')),
        (ELECTRONIC, _('Electronic')),
        (HOMELIKE, _('Homelike')),
        (FOOD, _('Food')),
        (CARS, _('Cars'),)
    )

    name = models.CharField(max_length=60)
    price = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images', default='images', blank=True, null=True)
    category = models.IntegerField(choices=CAT_TYPE, default=None, blank=True, null=True)

class auctionsform(ModelForm):

    class Meta:
        model = auctions
        fields = ('__all__')
        exclude = ('user',)
        widgets = {
            'name': TextInput(attrs={'placeholder':'Title'}),
            'description': TextInput(attrs={'placeholder':'Description'}),
            'initial_price': TextInput(attrs={'placeholder':'Price'}),
            'date': SelectDateWidget()
        }
