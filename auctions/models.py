from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms import ModelForm, SelectDateWidget, TextInput
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    pass

class Comment(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    auction_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)

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
    comment = models.ManyToManyField(Comment , blank=True)

    def comments_all(self):
        return ', '.join([a.comment_all for a in self.comment.all()])
    comments_all.short_description = "comments_all"

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

class auc_bid(models.Model):
    user = models.CharField(max_length=60)
    price = models.IntegerField()
    auc_id =  models.IntegerField()
    date = models.DateTimeField(auto_now=True)

class auc_bid_form(ModelForm):
    class Meta:
        model = auc_bid
        fields = ('__all__')
