from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from appdata.models import *
from django.contrib.auth.hashers import make_password


def dashboard(request, auctionid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    elif request.session.get("username") != auctionid:
        return HttpResponseRedirect('/')
    else:
        auctions = Auction.getAuctionByAdminId(request.session["id"])
        return render(request, "auction_admin.html", {'auctions':auctions})

def home(request):
    return render(request,"index.html",{})

def login(request):
    if request.session.get("username"):
        return HttpResponseRedirect('auction/'+request.session.get("id")+'/dashboard')
    if(request.method == "POST"):
        # try:
        print(request.POST)
        email = request.POST.get("email")
        password = request.POST.get('pwd')
        admin = Auction_admin.getAdmin(email,password)
        if(admin):
            request.session["username"] = admin.username
            request.session["id"] = admin.id
            return HttpResponseRedirect('/auction/'+str(admin.username)+'/dashboard')  
        else:
            return HttpResponse(content="User Does Not Exists")  
        # except Exception as e:
        #     # return HttpResponseRedirect('/')
        #     return HttpResponse(content=e)
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
    try:

        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            username = request.POST["username"]

            admin = Auction_admin(email=email, password=password, username=username)
            admin.save()
            return HttpResponseRedirect('/login')
    except Exception as r:
        return HttpResponse(content="User Already exists, please try with another id, or login")
    return render(request, "register.html", {})

def liveAuction(request,auctionid):
    return HttpResponse(content="Login Page")

def viewAuction(request,auctionid):
    auction = Auction.objects.get(id=auctionid)
    print(auction)
    return render(request, "view_auction.html", {'auction':auction})

def finalAuction(request,auctionid):
    return HttpResponse(content="Login Page")

def auctionsetup(request,auctionid):
    auction = Auction.objects.filter(id=auctionid)
    if(auction):
        auction = auction[0]
        if(auction.admin.id != request.session.get("id")):
            return HttpResponse(content="Unauthorize user")
        
    if request.method == "POST":
        
        return render(request, "auction_setup.html", {"auction":auction})
    else:
        print(auction.admin)
        return render(request, "auction_setup.html", {"auction":auction})

def allAuctions(request):
    auctions = Auction.getAll()
    content = ""
    if len(auctions) != 0:
        for i in auctions:
            content += i.auctionName
    else:
        content = "No Auctions organized yet"
    return render(request, "all_auction.html",{"auctions":auctions})

def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/')

