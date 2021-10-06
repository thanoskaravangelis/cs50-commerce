from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import Category, Listing, User



def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all()
    })


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

def create_listing(request):
    if request.method == "POST":
        imageEx = categoryEx = False
        user = User.objects.get(pk=1)
        if request.POST["title"]:
            title = request.POST["title"]
        else :
            return render(request, "auctions/create_listing.html",{
                "message" : "You did not provide a title!",
                "categories" : Category.objects.all()
            })  
        if request.POST["text"]: 
            text = request.POST["text"]
        else : 
            return render(request, "auctions/create_listing.html",{
                "message" : "You did not provide description text!",
                "categories" : Category.objects.all()
            })  
        if request.POST["starting_bid"]:
            starting_bid = request.POST["starting_bid"]
        else:
            return render(request, "auctions/create_listing.html",{
                "message" : "You did not provide a starting bid!",
                "categories" : Category.objects.all()
            })  
        if request.FILES.get("image"):
            image = request.FILES.get("image")
            imageEx = True
        if request.POST["category"]:
            category = Category.objects.get(name=request.POST["category"])
            categoryEx = True
        
        if imageEx :
            if categoryEx:
                l = Listing.objects.create(user = user,title = title,description = text,starting_bid = starting_bid,image = image,category = category)
            else:
                l = Listing.objects.create(user = user,title = title,description = text,starting_bid = starting_bid,image = image)
        else:
                l = Listing.objects.create(user = user,title = title,description = text,starting_bid = starting_bid)

        l.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create_listing.html",{
            "categories" : Category.objects.all()
        })   

def display_listing(request, listing_id):
    l = Listing.objects.get(pk=int(listing_id))
    if request.user.is_authenticated:
        if l in request.user.watchlist.all():
            s = True
        else :
            s = False
    else :
        s = False
    
    return render(request, "auctions/listing.html", {
        "listing" : l,
        "bids" : l.listing_bids.all(),
        "saved" : s
    })

@login_required
def addtowatch(request,listing_id):
    l = Listing.objects.get(pk=int(listing_id))
    
    request.user.watchlist.add(l)

    return display_listing(request,listing_id)

@login_required
def removefromwatch(request,listing_id):
    l = Listing.objects.get(pk=int(listing_id))
    
    request.user.watchlist.remove(l)

    return display_listing(request,listing_id)

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories" : Category.objects.all()
    })

def category_listings(request,cat_name):
    return render(request,"auctions/index.html", {
        "category" : cat_name,
        "listings" : Category.objects.get(name=cat_name).listings.all()
    })

@login_required
def watchlist(request,user_id):
    u = request.user
    all_listings = u.watchlist.all()
    return render(request,"auctions/watchlist.html", {
        "count" : all_listings.count(),
        "listings" : all_listings,
        "user_id" : int(user_id)
    })

@login_required
def remove_from_watchlist(request,user_id,listing_id):
    try:
        l = Listing.objects.get(pk = int(listing_id))
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: this listing does not exist")
    request.user.watchlist.remove(l)
    
    return HttpResponseRedirect(reverse("watchlist",args={user_id}))


