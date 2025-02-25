from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
import pyrebase


FIREBASE_CONFIG = {
    'apiKey': "AIzaSyDfd-F5xrs0m-2iyiWYTATlbTY3Hbv34JM",
    'authDomain': "votingsystem-eac2c.firebaseapp.com",
    'databaseURL': "https://votingsystem-eac2c.firebaseio.com",
    'projectId': "votingsystem-eac2c",
    'storageBucket': "votingsystem-eac2c.firebasestorage.app",
    'messagingSenderId': "1042982969135",
    'appId': "1:1042982969135:web:09165ebdead2a4145d4bda",
    'measurementId': "G-6XEJ7MJ7LX"
}

def firebase_instance():
    return pyrebase.initialize_app(FIREBASE_CONFIG)

@login_required
def admin_overview_view(request):
    return render(request, "myapp/admin_overview.html")


def login_view(request):
    firebase = firebase_instance()
    auth = firebase.auth()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # Assuming role information is stored somewhere accessible, e.g., session, database, or custom claim in Firebase
            user_info = auth.get_account_info(user['idToken'])
            is_admin = user_info['users'][0].get('isAdmin', False)
            
            if is_admin:
                return redirect("admin_overview")
            else:
                return redirect("overview")
        except:
            return render(request, "myapp/login.html", {"error": "Firebase authentication failed"})
    
    return render(request, "myapp/login.html")


# Home Page View
def home_view(request):
    return render(request, "myapp/home.html")  # ✅ Ensure home.html exists inside templates/myapp/

# Overview Page View (Requires Login)
@login_required
def overview_view(request):
    return render(request, "myapp/overview.html")

def logout_view(request):
    # Assuming you're using sessions or similar for storing the user session
    request.session.flush()
    return redirect('login')

def register_view(request):
    firebase = firebase_instance()
    auth = firebase.auth()

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            auth.create_user_with_email_and_password(email, password)
            # Here we can show a message to the user instead of redirecting
            return render(request, "myapp/register_success.html", {"message": "Pinoproseso pa ang iyong account"})
        except:
            return render(request, "myapp/register.html", {"error": "Firebase registration failed"})

    return render(request, "myapp/register.html")

