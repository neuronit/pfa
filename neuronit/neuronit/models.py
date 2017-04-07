from django.db import models
from django.contrib import admin
import os


def get_image_path(instance, filename):
    return os.path.join('images_carousel', str(instance.id), filename)


class Carousel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    intro_text = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=200, null=True)
    link_text = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.title

class LearnLink(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title

class LearnPresentation(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return ""

class CarouselAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'intro_text', 'link', 'link_text', 'image']
    search_fields = ['title']

class LearnLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'link']
    search_fields = ['title']

class LearnPresentationAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    search_fields = ['id']

admin.site.register(Carousel, CarouselAdmin)
admin.site.register(LearnLink, LearnLinkAdmin)
admin.site.register(LearnPresentation, LearnPresentationAdmin)
