from django.db import models
from django.contrib import admin


class ContactMails(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()

    def __str__(self):
        return self.email


class ContactMailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    search_fields = ['id']


admin.site.register(ContactMails, ContactMailsAdmin)
