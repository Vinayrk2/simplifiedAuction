from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import numpy as np

# Create your models here.
class Auction_admin(models.Model):
    username = models.CharField(max_length=40)
    # date = models.DateField()
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)

    def save(self):
        self.password = make_password(self.password)
        super().save()
    def __str__(self):
        return self.username
    
    @staticmethod
    def getAdmin(email,password):
        obj = Auction_admin.objects.filter(email=email)
        if(len(obj) == 1):
            obj = obj[0]
            if(check_password(password, obj.password)):
                return obj
        return None
    
class Auction(models.Model):
    auction = models.CharField(max_length=30, unique=True, null=False)
    auctionName = models.CharField(max_length=50, default='')
    admin   = models.ForeignKey('Auction_admin', on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)
    initialPoint = models.IntegerField(default=0)
    maxBid = models.IntegerField(default=0)
    location = models.CharField(max_length=50)
    status  = models.SmallIntegerField(default=0)
    # team  = models.ManyToManyField('Team', through='Auction_teams')
    def __str__(self):
        return self.auctionName    
    def startAuction(self):
        self.status = 1
    def endAuction(self):
        self.status = 2
    @staticmethod
    def getAll():
        return Auction.objects.all()
    @staticmethod
    def getAuctionByAdminId(adminid):
        admin = Auction.objects.filter(admin=adminid)
        return admin

class AuctionPlayer(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)
    team = models.ForeignKey('Team', on_delete=models.DO_NOTHING, null=True, blank=True)
    def __str__(self):
        return f"{self.auctionId} - {self.playerId}"
    
    def getRandomPlayer(self):
        players = Player.objects.filter(auction=auction)
        count = players.count()

        if(count == 0):
            return None
        flag = 0
        player = None
        auctionPlayer = None 

        while(flag != 1):
            randomIndex = np.random.randint(0,count)
            player = players[randomIndex]
            auctionPlayer = AuctionPlayer.objects.get(player = player)
            if(auctionPlayer.status == 0):
                flag = 1

        return player
    
    def finalizePlayer(self,team):
        self.team = Team.objects.filter(id=team)
        self.status = 1





class Player(models.Model):
    name         = models.CharField(max_length=30)
    category     = models.CharField(max_length=50)
    age          = models.IntegerField(null=True)
    battingStyle = models.TextField(null=True, default='')
    bowlingStyle = models.TextField(null=True, default='')
    gender       = models.SmallIntegerField(null=True)
    image        = models.ImageField( upload_to="player/", default='', null=True)
    def __str__(self):
        return self.name
    

    

class Team(models.Model):
    name    = models.CharField(max_length=35)
    logo    = models.ImageField(upload_to="team/",default=None, null=True)
    captainId = models.OneToOneField('Player', on_delete=models.DO_NOTHING, null=True, default=None)
    def __str__(self):
        return self.name