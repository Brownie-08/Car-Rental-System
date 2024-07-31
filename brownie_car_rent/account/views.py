# views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserLoginForm, UserRegisterForm, EmailVerificationForm



User = get_user_model()

# def send_verification_email(user):
#     code = get_random_string(6, allowed_chars='0123456789')
#     user.verification_code = code
#     user.save()
#     send_mail(
#         'Verify your email',
#         f'Your verification code is {code}',
#         'from@example.com',
#         [user.email],
#         fail_silently=False,
#     )

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.is_active = True  # User is inactive until email is verified
        user.save()
        return redirect('/login/')  # Redirect to login page after registration..... After hosting remove this to be able to authenticate a code to activate account
        # send_verification_email(user)
        # return redirect('verify_email')  # Redirect to email verification page

    context = {
        "title": "Registration",
        "form": form,
    }
    return render(request, "form.html", context)


# def verify_email_view(request):
#     form = EmailVerificationForm(request.POST or None)
#     if form.is_valid():
#         code = form.cleaned_data.get('code')
#         try:
#             user = User.objects.get(verification_code=code)
#             user.is_active = True
#             user.email_verified = True
#             user.verification_code = ''
#             user.save()
#             login(request, user)
#             return redirect('/car/newcar/')
#         except User.DoesNotExist:
#             form.add_error('code', 'Invalid verification code')

#     context = {
#         "title": "Verify Email",
#         "form": form,
#     }
#     return render(request, "verify_email.html", context)


def admin_register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # Admin should be active immediately
        user.save()

        return redirect('/login/')
    
    context = {
        "title": "Admin Registration",
        "form": form,
    }
    return render(request, "form.html", context)



def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin_dash/')
            else:
                return redirect('/car/newcar/')
    
    context = {
        "form": form,
        "title": "Login",
    }
    return render(request, "form.html", context)

def logout_view(request):
    logout(request)
    return render(request, "home.html", {})
