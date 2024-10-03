from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def chatpage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("loginpage")
    context = {}
    return render(request, "chatpage.html", context)
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get() to avoid KeyError
        password = request.POST.get('password')  # Use .get() to avoid KeyError
        if username and password:  # Check if both fields are filled
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chatpage')  # Redirect to chat page on successful login
            else:
                return render(request, 'loginpage.html', {'error': 'Invalid login credentials'})
        else:
            return render(request, 'loginpage.html', {'error': 'Both fields are required.'})
    return render(request, 'loginpage.html')
def logout_user(request):
    logout(request)  # Log the user out
    return redirect('loginpage')  # Redirect to the login page after logging out