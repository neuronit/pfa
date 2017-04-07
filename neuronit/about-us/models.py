from django.db import models
from django.contrib import admin
import os

class DescriptionP(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()

    def __str__(self):
        return self.content

class DescriptionPAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']
    search_fields = ['id']


def get_image_path(instance, filename):
    return os.path.join('images_profile', str(instance.id), filename)

class TeamMember(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    title = models.CharField(max_length = 200)
    description_text = models.TextField(blank=True, null=True)

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'title', 'description_text']
    search_fields = ['name', 'title']


admin.site.register(DescriptionP, DescriptionPAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
