from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl

def send_email(request,user,email_subject='Please activate yout foodOnine account',email_temp='accounts/emails/account_verification_email.html'):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site=get_current_site(request)
    mail_subject=email_subject
    message=render_to_string(email_temp,{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),   ###encode user's primary key
        'token':default_token_generator.make_token(user),
    })
    to_email=user.email
    mail=EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()

# def send_password_reset_email(request,user):
#     from_email=settings.DEFAULT_FROM_EMAIL
#     current_site=get_current_site(request)
#     mail_subject='Reset your password'
#     message=render_to_string('accounts/emails/reset_password_email.html',{
#         'user':user,
#         'domain':current_site,
#         'uid':urlsafe_base64_encode(force_bytes(user.pk)),   ###encode user's primary key
#         'token':default_token_generator.make_token(user),
#     })
#     to_email=user.email
#     mail=EmailMessage(mail_subject,message,from_email,to=[to_email])
#     mail.send()
