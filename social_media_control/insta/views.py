from django.shortcuts import render, HttpResponse, redirect
from insta.apps import driver
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index_page(request):
    return HttpResponse("Site Is Working")



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the user's dashboard
        else:
            error_message = "Invalid username or password"
    else:
        error_message = None

    return render(request, 'login.html', {'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect('login')