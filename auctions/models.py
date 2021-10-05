from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ModelForm, SelectDateWidget, TextInput

class User(AbstractUser):
    pass

class auctions(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images', default='images', blank=True, null=True)

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
