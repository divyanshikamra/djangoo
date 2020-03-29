from django.shortcuts import render,redirect, get_object_or_404
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .import forms
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def articles_list(request):
    if request.method =='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            articles= Article.objects.all().order_by('date')
            return render(request,"articles/loggedin.html", {'User' :user, 'articles':articles })
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

    else:
        form=AuthenticationForm()

    articles= Article.objects.all().order_by('date')
    return render(request,'articles/article_list.html',{'articles': articles, 'form':form})

def article_detail(request, slog):
    article= Article.objects.get(slog=slog)
    user= request.user
    return render(request, 'articles/article-detail.html',{'article':article, 'user':user})

@login_required(login_url="/articles")
def logged_in(request):
    user=request.user
    articles=Article.objects.all().order_by('date')
    return render(request,"articles/loggedin.html", {'User' :user, 'articles':articles })

@login_required(login_url="/articles")
def article_create(request):
    if request.method=="POST":
        form=forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            #save article to db
            instance=form.save(commit=False)
            instance.author=request.user
            instance.save()
            return redirect("detail", slog=instance.slog)
    else:
        form= forms.CreateArticle()
    return render(request,'articles/article_create.html',{'form':form})

def edit_post(request, slog):
 template= 'articles/article_create.html'
 post= get_object_or_404(Article,slog=slog)
 if request.user==post.author:
    if request.method== 'POST':
        form= forms.CreateArticle(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post= form.save(commit=False)
            post.author= request.user
            post.save()
            messages.success(request,"Your blog has been editted!")
            return redirect("detail", slog=post.slog)
    else:
        form=forms.CreateArticle(instance=post)
    return render(request, template,{'form':form})
 else:
     messages.success(request,"You can only edit your blogs!")
     return redirect("loggedin")

def delete_post(request, slog):
    post=get_object_or_404(Article, slog=slog)
    post.delete()
    messages.success(request, "Successfully Deleted")
    return redirect('loggedin')
