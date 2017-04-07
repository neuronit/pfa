
from django.db import models
from datetime import date
from django.contrib import admin
from django.forms import ModelForm, Textarea
from django.core.validators import MinValueValidator
# Create your models here.


class Reseau(models.Model):

    
    mlp="mlp"
    elman='elman'
    jordan='jordan'
    select= 'select_type'
    op_tempo= 'op_tempo'
    op_plus= 'op_plus'
    op_minus= 'op_minus'
    op_divide= 'op_divide'
    op_avg= 'op_avg'
    op_recomp= 'op_recomp'
    op_decomp= 'op_decomp'
    network_choices=(
        (select,'select'),
        (mlp, "MLP"),
        (elman,'Elman'),
        (jordan,'Jordan'),
        (op_tempo,'Temporize'),
        (op_plus, 'Add'),
        (op_minus,'Substract'),
        (op_divide,'Divide'),
        (op_avg,'Average'),
        (op_recomp,'Recomposite'),
        (op_decomp,'Decomposite'),
        )
    #help_text to be written for in popup for each parameter


                               
    
    type= models.CharField(max_length=100,choices=network_choices,default="select",help_text="type involving different behavior of your network")

    
    weight= models.FloatField(null=True,blank=True,verbose_name='weight scaling',help_text="weight influence for each iteration")
    victory= models.FloatField(null=True,blank=True,verbose_name='victory reward',help_text="reward at each game won")
    defeat= models.FloatField(null=True,blank=True,verbose_name='defeat punishement',help_text="punishement for each lost game")
    network_layers=models.CharField(null=True,blank=True,verbose_name='hidden layers',max_length=16,help_text="number of hidden layers for a given network, format: *,*,...,*, . Unexpecting behavior if incorrect form")

    def __str__(self):
        return self.type


class Reseau_info(models.Model):
    network_name=models.CharField(max_length=100,default="")
    info=models.CharField(max_length=300,default="toto")
    
    
    def __str__(self):
        return self.network_name


class Game(models.Model):
    game_id = models.IntegerField(default=0, primary_key=True)
    game_name = models.CharField(max_length=200)
    info = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.game_name
                                     

class Save(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='saves/')
    game = models.ForeignKey(Game)
    player_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, default="Unknown")

    def __str__(self):
        return ""


class Score(models.Model):

    id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=200)
    game = models.ForeignKey(Game)
    score = models.IntegerField(default=0)
    date = models.DateField("Date", default=date.today)

    def __str__(self):
        return self.player_name


class BestScore(models.Model):
    id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=200)
    game = models.ForeignKey(Game)
    best_score = models.IntegerField(default=0)
    date = models.DateField("Date", default=date.today)

    def __str__(self):
        return self.player_name

class SaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file', 'game', 'player_name', 'date']
    search_fields = ['player_name', 'game', 'name']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'player_name', 'game', 'score', 'date']
    search_fields = ['player_name', 'game']


class BestScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'player_name', 'game', 'best_score', 'date']
    search_fields = ['player_name', 'game']

admin.site.register(Save, SaveAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(BestScore, BestScoreAdmin)




class ReseauForm(ModelForm):
    class Meta:
        model = Reseau
        fields= ['type','weight','victory','defeat','network_layers']
        widgets = {

            }




        
