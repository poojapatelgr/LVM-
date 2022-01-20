from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import TokenForm
from leaveman.models import Profile
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


# Create your views here.
@login_required
def index(request):
    return render(request,'leaveman/index.html')
    #return HttpResponseRedirect(reverse("students:signin"))

def registration(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'tokenauth/index.html')
    context['form']=form
    return render(request,'registration/registration.html',context)

def tokenlogin(request):
    if request.method == 'POST':
        token = request.POST['token']
        print(token)
        profile=get_object_or_404(Profile,token=token)
        print('profile',profile)
        request.user=User.objects.get(username=profile.user)
        print(request.user)
        login(request,request.user)
        #return render(request,'tokenauth/index.html')
        #return HttpResponseRedirect('leaves/')
        #return render(request,'leaves/base.html',context)
        #return redirect('tokenauth:index')
        return HttpResponseRedirect(reverse("leaveman:index"))
        #return HttpResponseRedirect(reverse('leaveman:index'))
    else:
        form=TokenForm()
        return render(request,'tokenauth/tokenlogin.html',{'form':form})

def tokenloginurl(request,token):
        #token = request.POST['token']
        #print(token)
        profile=get_object_or_404(Profile,token=token)
        print('profile',profile)
        request.user=User.objects.get(username=profile.user)
        print(request.user)
        login(request,request.user)
        #return render(request,'tokenauth/index.html')
        #return HttpResponseRedirect('leaves/')
        #return render(request,'leaves/base.html',context)
        return HttpResponseRedirect(reverse('leaveman:index'))
    #else:
        #form=TokenForm()
        #return render(request,'tokenauth/tokenlogin.html',{'form':form})

