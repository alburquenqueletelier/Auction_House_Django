from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import *


def index(request):
    all_auctions = auctions.objects.all()
    context = {
        "all_a" : all_auctions
    }
    return render(request, "auctions/index.html", context)


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
    context = {
        'see' : see
    }
    return render(request, "auctions/auc_bid.html", context)

def addcomment(request,pk):
    auc_id = pk

    if request.method == 'POST':
        auction = auctions.objects.get(pk=pk)
        auc_user = auction.user
        owner = request.POST["owner"]
        author = request.POST["author"]
        comment = request.POST["comment"]
        new_comment = auction.comment.create(content=comment, user_id=owner, auction_id=auc_id, author=author)

        return redirect("see_auction", pk=auc_id)

    return redirect ("see_aucton", pk=auc_id)

