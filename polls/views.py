from django.shortcuts import redirect, render
from django.http import Http404,HttpResponseRedirect, request, response
import datetime as dt
from .models import Article, NewsLetterRecipients
from .forms import NewsLetterForm,NewArticleForm
from.email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from decouple import config
from django.http import JsonResponse
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import MoringaMerch
from .serializer import MerchSerializer
from rest_framework import status
from.permissions import IsAdminOrReadOnly
from polls import serializer
# Create your views here.

class MerchList(APIView):
    def get(self,request,format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        permission_classes = (IsAdminOrReadOnly,)
        return Response(serializers.data)
        
    def post(self,request,format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_merch(self,pk):
        try:
            return MoringaMerch.objects.get(pk=pk)
        except MoringaMerch.DoesNotExist:
            return Http404

    def get(self,request,pk,format=None):
        merch = self.get_merch(pk)
        serilizers = MerchSerializer(merch)
        return Response(serilizers.data) 

    def put (self,request,pk,format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    article = Article.objects.all()
    ctx = {'article':article}
   
    return render(request, 'welcome.html',ctx)


def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date":date,"news":news,"letterForm":form})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')
    recipient = NewsLetterRecipients(name=name,email=email)
    recipient.save()
    user = authenticate(name,email)
    if user is not None:
        send_welcome_email(name,email)
        messages.add_message(request, messages.SUCCESS, "Registered successfully")
    data = {'success':"You have been successfully added to mailing list"}
    return JsonResponse(data)
    
def past_days_news(request,past_date):
    try:
       date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
    except ValueError:
        raise Http404()
        assert False
    if date == dt.date.today():
        return redirect(news_today)
    news = Article.days_news(date)
    return render(request,'all-news/past-news.html', {"date":date,"news":news})


def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"
        return render(request,'all-news/search.html',{"message":message,"articles":searched_articles})
    else:
        message = "You haven't serahced for ant term"
        return render(request,'all-news/search.html',{"message":message})
 

@login_required(login_url='/accounts/login/')
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ValueError:
        raise Http404()
    return render(request,"all-news/article.html",{"article":article})

@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newsToday')

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("all-news/today-news.html")