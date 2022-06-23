from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from list.models import *
from list.forms import *
from django.contrib import auth
from datetime import datetime

# Create your views here.

class BaseView(View):
    views = {}

class HomeView(BaseView):
    def get(self,request):
        return render(request, 'home.html')

class TodoView(BaseView):
    login_required = True
    def get(self, request):
        self.views['date'] = datetime.now()
        username = request.user.username
        self.views['todos'] = Todo_List.objects.filter(username = username)
        return render(request, 'todo.html', self.views)

    def post(self,request):
        username = request.user.username
        user = request.user
        todo = request.POST['todo']

        if not todo:
            messages.error(request, 'input field is required')
            return redirect('list:todo')
        if user is None:
            messages.error(request, "You are not registered yet")
            return redirect('list:signup')

        list = Todo_List.objects.create(
                username = username,
                title = todo
                )
        list.save()
        messages.success(request, "New todo created successfully")
        return redirect('list:todo')

   


def signup(request):
    if request.method == "POST":
        fm = SignupForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "You are registered successfully")
            return redirect('list:login')
    else:
        fm = SignupForm()
    return render(request, 'signup.html',{'fm':fm})
        

    # return render(request, 'signup.html' {'form':fm})


def login(request):
    if request.user.is_authenticated:
        return redirect('list:todo')
    if request.method == "POST":
        # fm = AuthenticationForm()
        fm = AuthenticationForm(request = request ,data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data['username']
            pw = fm.cleaned_data['password']
            user = auth.authenticate(username = username, password = pw)
            if user is not None:
                auth.login(request, user)
                return redirect('list:todo')
    else:
            fm = AuthenticationForm()
    return render(request,'login.html', {'form':fm})

def profile(request):
    user = request.user
    if user.is_authenticated:
     return render(request, 'profile.html')
    else:
        return redirect('list:home')

def delete(request, pk):
        id = pk
        todo = Todo_List.objects.get(id = id)
        todo.delete()
        return redirect('list:todo')

def update(request, pk):
    if request.method == 'POST':
        id = pk
        username = request.user.username
        title = request.POST['add']

        if not title:
            messages.error(request, 'this field is required')
            return redirect('list:update')

        Todo_List.objects.filter(id = id, username = username).update(id = id, username = username, title = title)
        messages.success(request, "todo updated successfully")
        return redirect('list:todo')
    # title = Todo_List.objects.get(id = id).title
    return render(request, 'edit-todo.html')

def logout(request):
    auth.logout(request)
    return redirect('list:home')


def complete(request, pk):
    username = request.user.username
    id = pk
    # list = Todo_List.objects.get(id = id)
    Todo_List.objects.filter(id = id, username = username).update(id = id, username = username, complete = True)
    return redirect('list:todo')