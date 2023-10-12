from django.shortcuts import render,HttpResponse
from .models import Contact
from django.contrib import messages
from blog.models import Post 
# Create your views here.

def home(request):
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request , 'home/home.html', context)


def about(request):
    return render(request , 'home/about.html')
    

def contact(request):
    # messages.error(request, "Welcome to contact!")
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']

        if len(name)<2 or len(email)==0 or len(email)<5 or len(phone)<10 or content==0:
            messages.error(request, "Please Fill all the details")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Thankyou for contacting with us our team mate will reach you with in 24hr.")
    return render(request, "home/contact.html")


def search(request):
    query=request.GET['query']
    allPosts= Post.objects.filter(title__icontains=query)
    params={'allPosts': allPosts}
    return render(request, 'home/search.html', params)
    