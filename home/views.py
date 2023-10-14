from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .models import Contact
from django.contrib import messages
from blog.models import Post 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout


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
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)




def handelSignup(request):
    if request.method == "POST":
        # get the post parameter
        username=request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # checks for check the inputs
        if len(username)<3 or len(fname)<3 or len(lname)<2 or len(email)<3 or len(pass1)<8 or len(pass2)<8:
            messages.error(request, "Please fill all the details carefully")
            return redirect('/')
        
        elif  len(pass1)!=len(pass2) or pass1!=pass2:
            messages.error(request, "Password Not Match, Please fill all the details carefully")
            return redirect('/')
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()

        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('/')
    else:
        return JsonResponse({"status":404, "message":"not found"})
        
    

def handelLogin(request):
    if request.method == "POST":
        # get the post parameter
        loginusername=request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(request,username=loginusername, password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request, "Successfully login")
            return redirect('/') 
        else:
            messages.error(request, "You have enter invalid credentials please check it and try again")
            return redirect('/')




def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logout")
    return redirect('/')