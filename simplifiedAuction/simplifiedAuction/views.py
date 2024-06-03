from django.http import HttpResponse
from django.shortcuts import render
from appdata.models import *
from django.contrib.auth.hashers import make_password


def dashboard(request, auctionid):
    return HttpResponse(content="Hello World")

def home(request):
    return render(request,"index.html",{})

def login(request):
    if(request.method == "GET"):
        return render(request, "login.html", {})
    else:
        return HttpResponse(content=request.POST["id"])

def createAuction(request):
    return render(request, "create_auction.html", {})

def addPlayer(request):
    return render(request, "create_auction.html", {})

def addTeam(request):
    return render(request, "create_auction.html", {})

def myAuctions(request):
    return render(request, "create_auction.html", {})

def register(request):
    return HttpResponse(content="Login Page")

def auction(request,auctionid):
    return HttpResponse(content="Login Page")

def finalAuction(request,auctionid):
    return HttpResponse(content="Login Page")
