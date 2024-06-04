from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from appdata.models import *
from django.contrib.auth.hashers import make_password


def dashboard(request, auctionid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    return HttpResponse(content="Hello World")

def home(request):
    return render(request,"index.html",{})

def login(request):
    if request.session.get("username") != None:
        return HttpResponseRedirect('auction/'+request.session.get("id")+'/dashboard')
    if(request.method == "POST"):
        auction = Auction_admin.objects.get(email=request.POST['email'])

        if(auction):
            request.session["username"] = auction.username
            return HttpResponseRedirect('/auction/'+auction.username+'/dashboard')  
        else:
            return HttpResponse(content="User Does Not Exists")  
        return HttpResponseRedirect('/')
    else:
        return render(request, "login.html", {})

def createAuction(request):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    return render(request, "create_auction.html", {})

def addPlayer(request, auctionid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    return render(request, "create_auction.html", {})

def addTeam(request, auctionid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    return render(request, "create_auction.html", {})

def myAuctions(request):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    return render(request, "create_auction.html", {})

def register(request):
    if request.session.get("username") != None:
        return HttpResponseRedirect('auction/'+request.session.get("id")+'/dashboard')
    
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        username = request.POST["username"]

        admin = Auction_admin(email=email, password=password, username=username)
        admin.save()
        return HttpResponseRedirect('/login')
    return render(request, "register.html", {})

def liveAuction(request,auctionid):
    return HttpResponse(content="Login Page")

def finalAuction(request,auctionid):
    return HttpResponse(content="Login Page")

def allAuctions(request):
    auctions = Auction.getAll()
    content = ""
    if len(auctions) != 0:
        for i in auctions:
            content += auctions.id
    else:
        content = "No Auctions organized yet"
    return HttpResponse(content=content)

