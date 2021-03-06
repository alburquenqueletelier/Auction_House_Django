from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import datetime as dt


from .models import *


def index(request):
    all_auctions = auctions.objects.filter(state=True)
    context = {
        "all_a" : all_auctions
    }
    return render(request, "auctions/index.html", context)

def closed(request):
    all_auctions = auctions.objects.filter(state=False)
    bids = bid.objects.all()
    user_bids = User.objects.all()
    context = {
        "all_a" : all_auctions,
        'bids' : bids,
        'user_bids' : user_bids
    }
    return render(request, "auctions/closed.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_auction(request):

    if request.method == "POST":
        form = auctionsform(request.POST, request.FILES, request.user)
        if form.is_valid():
            ins = form.save(commit=False)
            ins.user = request.user
            ins.state = True
            ins.init_price = ins.price
            if not request.user == ins.user:
                raise Http404
            ins.save()
            form = auctionsform()
            context = {
                "form" : form
            }
            messages.success(request, 'Form submission successful')
            return render(request,"auctions/new_ac.html", context)
    else:
        form = auctionsform()
        context = {
            "form" : form
        }
        return render(request, "auctions/new_ac.html", context)

def see_auction(request,pk):
    see = auctions.objects.get(pk=pk)
    user = request.user
    if wlist.objects.filter(user=user.id, auc_id = pk):
        watch_status = True
    else:
        watch_status = False
    try:
        bid_see = bid.objects.get(auc_id=pk)
        user_bid = User.objects.get(pk=bid_see.user)
    except:
        bid_see = None
        user_bid = None
        pass
    
    context = {
        'see' : see,
        'bid_see' : bid_see,
        'user_bid' : user_bid,
        'w_s' : watch_status
    }
    return render(request, "auctions/auc_bid.html", context)

def addcomment(request,pk):
    if request.method == 'POST':
        auction = auctions.objects.get(pk=pk)
        owner = request.POST["owner"]
        author = request.POST["author"]
        comment = request.POST["comment"]
        new_comment = auction.comment.create(content=comment, user_id=owner, auction_id=pk, author=author)

        return redirect("see_auction", pk=pk)

    return redirect ("see_aucton", pk=pk)

def addbid(request,pk):
    auction = auctions.objects.get(pk=pk)
    if request.method == 'POST':
        actual_p = auction.price
        owner = request.POST["owner"]
        bid_h = int(request.POST["bid"])
        if bid_h > actual_p:
            try:
                bid_exist = bid.objects.get(auc_id=pk)
                if bid_exist.auc_id == auction.id:
                    bid.objects.filter(auc_id=pk).update(user=owner, bid_price=bid_h, auc_id=pk)
                    auctions.objects.filter(pk=pk).update(price=bid_h, winner=owner)
                    return redirect("see_auction", pk=pk)
            except:
                b_a = bid(user=owner, bid_price=bid_h, auc_id=pk)
                b_a.save()
                auctions.objects.filter(pk=pk).update(price=bid_h, winner=owner)
                return redirect("see_auction", pk=pk)
        else:
            return HttpResponse('<h2>Your offer is too low actual price is %s</h2>' % auction.price)
    
    return redirect("see_auction", pk=pk)
    
def closebid(request,pk):
    auctions.objects.filter(pk=pk).update(state=False)
    bid.objects.filter(auc_id=pk).update(date=dt.datetime.now())
    return redirect('index')

def categories(request):
    all_cat = auctions.CAT_TYPE
    context = {
        "all_cat" : all_cat
    }
    return render(request, "auctions/categories.html", context)

def cat_choose(request, cat_id):
    all_auctions = auctions.objects.filter(state=True, category = cat_id)
    context = {
        "all_a" : all_auctions
    }
    return render(request, "auctions/cat_choose.html", context)

def add_to_w(request,pk):
    auc = auctions.objects.get(pk=pk)
    user = request.user
    if wlist.objects.filter(user=user.id, auc_id = pk).exists():
        w_l = wlist.objects.filter(user=user.id, auc_id = pk)
        w_l.delete()
    else:
        w_l = auc.watchlist.create(user=user.id, auc_id=pk)
        w_l.save()
    return HttpResponseRedirect(reverse('see_auction', kwargs={'pk':pk}))

def watchlist(request):
    user = request.user
    #try:
    #all_auctions = auctions.objects.filter(user=2)
    all_auctions = auctions.objects.filter(watchlist__user = user.id, state = True)
    context = {
    'watch' : all_auctions
    }
    return render(request, "auctions/watchlist.html", context)
    #except:
     #   context = {
      #  'watch' : "No auction listing in watchlist"
       # }
        #return render(request, "auctions/watchlist.html", context)
