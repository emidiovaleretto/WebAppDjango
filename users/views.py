from django.shortcuts import render, redirect
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages

import threading


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if empty_field(name):
            messages.error(request, 'The item name cannot be empty.')
            return redirect('register')

        if empty_field(email):
            messages.error(request, 'The item email cannot be empty.')
            return redirect('register')

        if passwords_are_not_equal(password, password2):
            messages.error(request, 'Passwords are not equal.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email address is taken. Try another.')
            return redirect('register')

        if User.objects.filter(username=name).exists():
            messages.error(request, 'That username is taken. Try another.')
            return redirect('register')

        if len(password) < 8 or len(password) > 30:
            messages.error(request, 'Your password must be between 8 and 30 characters.')
            return redirect('register')

        if not validate_email(email):
            messages.error(request, 'Please provide a valid email')
            return redirect('register')

        user = User.objects.create_user(username=name, email=email, password=password)
        user.set_password(password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        email_subject = 'Active your Account'
        message = render_to_string('users/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
                                   )
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])

        EmailThread(email_message).start()
        messages.success(request, "Well Done!! Please check your email. We've sent you a link to confirm your "
                                  "account. :)")
        return redirect('login')

    else:
        return render(request, 'users/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')

    messages.error(request, 'Activation link is invalid!')
    return render(request, 'users/activate_failed.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if empty_field(email) or empty_field(password):
            messages.error(request, 'The fields cannot be empty.')

        if User.objects.filter(email=email).exists():
            name = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=name, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Opss, you have to confirm your email address. After your email is confirmed, '
                                        'return to this page to continue.')
        else:
            alert_message(request)

    return render(request, 'users/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def empty_field(field):
    return not field.strip()


def alert_message(request):
    messages.error(request, 'Incorrect email or password.')
    return redirect('login')


def passwords_are_not_equal(password, password2):
    return password != password2
