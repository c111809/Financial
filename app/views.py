from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect('/index')
        else:
            return render(request, 'app/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'app/login.html')

# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'app/register.html', {'form': form})
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        invite_code = request.POST.get('invite_code')
        if invite_code != 'cuijiayu123':
            messages.error(request, 'Invalid invite code.')
            return render(request, 'app/register.html', {'form': form})
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})


@login_required
def index_view(request):
    num1, num2, operator, result = None, None, None, None
    error_message = None
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1'))
            num2 = float(request.POST.get('num2'))
            operator = request.POST.get('operator')
            if operator == '+':
                result = round(num1 + num2, 8)
            elif operator == '-':
                result = round(num1 - num2, 8)
            elif operator == '*':
                result = round(num1 * num2, 8)
            elif operator == '/':
                result = round(num1 / num2, 8)
        except ValueError:
            error_message = 'Please enter a valid value.'
    return render(request, 'app/index.html', {'username': request.user.username, 'num1': num1, 'num2': num2, 'operator': operator, 'result': result, 'error_message': error_message})

