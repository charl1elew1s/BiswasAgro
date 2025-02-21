from django.shortcuts import render
from django.shortcuts import redirect


def home_page(request):
    # determine if a user is logged in, if not present them with the login page
    if 'user' in request.session:
        return render(request, 'home.html', {})

    return redirect('bisauth:login')
