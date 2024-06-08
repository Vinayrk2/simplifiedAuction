from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from appdata.models import *
from django.contrib.auth.hashers import make_password
# from .settings import MEDIA_ROOT, MEDIA_URL


def dashboard(request, adminid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    elif request.session.get("username") != adminid:
        return HttpResponseRedirect('/')
    else:
        auctions = Auction.getAuctionByAdminId(request.session["id"])
        return render(request, "auction_admin.html", {'auctions':auctions})

def home(request):
    return render(request,"index.html",{})

def login(request):
    if request.session.get("username"):
        return HttpResponseRedirect('auction/'+request.session.get("username")+'/dashboard')
    if(request.method == "POST"):
        # try:
        print(request.POST)
        email = request.POST.get("email")
        password = request.POST.get('pwd')
        admin = Auction_admin.getAdmin(email,password)
        if(admin):
            request.session["username"] = admin.username
            request.session["id"] = admin.id
            return HttpResponseRedirect('/auction/'+(admin.username)+'/dashboard')  
        else:
            return HttpResponse(content="User Does Not Exists")  
        # except Exception as e:
        #     # return HttpResponseRedirect('/')
        #     return HttpResponse(content=e)
    else:
        return render(request, "login.html", {})

def createAuction(request,adminid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    if request.method == "POST":
        return HttpResponseRedirect("/")
    auction=["auctionName","date","initialPoint","maxBid","location","status"]
    return render(request, "create_auction.html", {"auction":auction})

def addPlayer(request, auctionid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        age = request.POST.get("age")
        battingStyle = request.POST.get("battingStyle")
        bowlingStyle = request.POST.get("bowlingStyle")
        gender = request.POST.get("gender")
        image = request.FILES['image']
        try:
            if name != None and type != None and age != None and battingStyle != None and bowlingStyle != None and gender != None and image != None:
                player = Player()
                player.name = name
                player.category = category
                player.age = age
                player.battingStyle = battingStyle 
                player.bowlingStyle = bowlingStyle
                player.gender = 1 if gender == "male" else "female"
                player.image = image
                player.save()

                auction = Auction.objects.get(id=auctionid)
                auctionplayer = AuctionPlayer()
                auctionplayer.player = player
                auctionplayer.auction = auction
                auctionplayer.team = None
                auctionplayer.status= 0
                auctionplayer.save()
                return HttpResponseRedirect("/auction/{}/addplayer".format(auctionid))
        except Exception as e:
            return HttpResponseRedirect("/error/1")

    players = AuctionPlayer.objects.all()

    
    return render(request, "add_player.html", {"auctionid":auctionid, "players":players})

def addTeam(request, auctionid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    
    auction = Auction.objects.get(id=auctionid)
    if request.method == "POST":
        name = request.POST.get("name")
        logo = request.FILES['logo']

        team = Team()
        team.name = name
        team.logo = logo
        team.auction = auction
        team.save()

        return HttpResponseRedirect("/auction/{}/addteam".format(auctionid))
    teams = Team.objects.filter(auction = auction)
    return render(request, "add_team.html", {"auctionid":auctionid, "teams":teams})

def myAuctions(request,adminid):
    if request.session.get("username") == None:
        return HttpResponseRedirect('/login')
    else:
        auctions = Auction.getAuctionByAdminId(request.session["id"])
        return render(request, "all_auction.html", {"auctions":auctions})
      
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
    auction = Auction.objects.get(id=auctionid)

    if request.session.get("id") == auction.admin.id:
        if auction.status == 0:
            auction.startAuction()
            auction.save()
        elif auction.status == 1:
            return render(request, "live_auction.html", {"auction":auction})
        elif auction.status == 2:
            return HttpResponseRedirect("/auction/{}/final".format(auctionid))
        else:
            return HttpResponseRedirect("/auction/{}/final".format(auctionid))
    # auction = Auction.objects.get(id=auctionid)

    if auction.status == 1:
        return render(request, "live_auction.html", {"auction":auction})
    elif auction.status == 2:
        return HttpResponseRedirect("/auction/{}/final".format(auctionid))
    else:
        return HttpResponseRedirect("/auction/{}/dashboard".format(auctionid))
    
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
        auction = Auction.objects.get(id=auctionid)
        auction.auctionName = request.POST.get("auctionName")
        auction.date = request.POST.get("date")
        auction.initialPoint = request.POST.get("initialPoint")
        auction.maxBid = request.POST.get("maxBid")
        auction.location = request.POST.get("location")
        auction.status = request.POST.get("status")
        auction.save()
        # return render(request, "auction_setup.html", {"auction":auction})
    # else:
    auction = Auction.getAuctionInDict(auctionid)
    # print(auction.admin)
    return render(request, "auction_setup.html", {"auctionid":auctionid, "auction":auction})

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

def errorHandler(request,err):
    errs = {
        "1":"User Already Exists",
        "2":"Update is not possible due to mandatiry field deleted",
        "404":"The page not found"
    }
    return render(request, "error.html", {"err":errs[str(err)]})