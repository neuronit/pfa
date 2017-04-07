from django.shortcuts import render
from django.core.mail import send_mail
from .models import *


def contact(request):

    if request.method == 'GET':
        response_data = ""

    if request.method == 'POST':
        try:
            contact_list = ContactMails.objects.all()
            name = request.POST.get('name')
            subject = request.POST.get('subject')
            email = request.POST.get('email')
            message = request.POST.get('message')

            text = "SENT FROM: Neuron It contact page\n"
            text += "     FROM: " + email + "\n"
            text += "     SUBJECT: " + subject + "\n"
            text += "     NAME: " + name + "\n"
            text += message + "\n"

            send_mail(
                "New Inquiry",
                text,
                email,
                contact_list,
                fail_silently=False
            )
            print("Log: Success!")
            response_data = "Thank you for contacting us!"
        except Exception as e:
            response_data = str(e)
    return render(request, 'contact/contact.html', {'response': response_data})
