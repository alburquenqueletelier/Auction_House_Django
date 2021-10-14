from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ModelForm, SelectDateWidget, TextInput
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pass

class auctions(models.Model):
    SPORT = 'Sport'
    ELECTRONIC = 'Electronic'
    HOMELIKE = 'Homelike'
    FOOD = 'Food'
    CARS = 'Cars'

    CAT_TYPE = (
        (SPORT, _('SPORT')),
        (ELECTRONIC, _('ELECTRONIC')),
        (HOMELIKE, _('HOMELIKE')),
        (FOOD, _('FOOD')),
        (CARS, _('CARS'),)
    )

    name = models.CharField(max_length=60)
    price = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images', default='images', blank=True, null=True)
    category = models.CharField(max_length=15, choices=CAT_TYPE, default=None, blank=True, null=True)

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
