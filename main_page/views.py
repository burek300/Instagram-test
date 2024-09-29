# import libraries
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Following, Messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
import shutil
from django.http import JsonResponse
from django.urls import reverse


def delete_all_files_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return
    
    # Get the list of all files and directories in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file and delete it
        if os.path.isfile(file_path) or os.path.islink(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        elif os.path.isdir(file_path):
            try:
                shutil.rmtree(file_path)
                print(f"Deleted directory: {file_path}")
            except Exception as e:
                print(f"Failed to delete directory {file_path}. Reason: {e}")

@login_required
def index(request):
    user = request.user
    user_dict = {"user": user}
    return render(request, "index.html", user_dict)

@login_required
def profile(request):
    user = request.user
    context = {}
    context["user"] = user
    return render(request, "profile.html", context)

@login_required
def comments(request): 
    return render(request, "comments.html")

@login_required
def followers(request):
    return render(request, "followers.html")

@login_required
def post(request):
    return render(request, "post.html")

@login_required
def search_users(request):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        query = request.GET.get("query", "")
        if query:
            users = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
            users_list = [
                {
                    "username": user.username,
                    "profile_image":user.profile_image.url if user.profile_image else None,
                    "profile_url": reverse("user_profile", args=[user.username])
                }
                for user in users
            ]
        else:
            users_list = []

        return JsonResponse(users_list, safe=False)
    return render(request, "search.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        try:
            user = CustomUser.objects.get(email=email)
            username = user.username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks in seconds
                else:
                    request.session.set_expiry(0)  # Browser close

                return redirect("index")
            else:
                messages.error(request, "Invalid username or password")
        except CustomUser.DoesNotExist:
            messages.error(request, "User with this email does not exist")
    
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, "Email is already used")
        elif CustomUser.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
        else:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.first_name = full_name
            user.profile_image = "default_profile.png"
            user.save()
            return redirect("login")
        return render(request, "register.html")
    else:
        return render(request, "register.html")
    
def logout_view(request):
    logout(request)
    return redirect("login")

def redirect1(request):
    return redirect("login")

@login_required
def edit_profile(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        username = request.POST.get("username")
        description = request.POST.get("description")
        privacy = request.POST.get("privacy")
        current_image = request.POST.get("current_image")
        if privacy == "private":
            tf = True
        else:
            tf = False
        user = CustomUser.objects.get(username=username)
        if not image:
            folder_path = os.path.join('profile_images', str(user.id))
            delete_all_files_in_folder(folder_path)
            if current_image:
                image = current_image
            else:
                image = "default_profile.png"
        user.profile_image = image
        user.description = description
        user.is_private = tf
        user.save()
        return redirect("myprofile")
    return render(request, "edit_profile.html")

def user_profile(request, username):
    user = CustomUser.objects.get(username=username)
    is_following = request.user.following.filter(following_user=user).exists()

    context = {
        "user": user,
        "is_following":is_following,
    }
    return render(request, "different_profile.html", context)

def follow_unfollow(request, username):
    if request.method == "POST":
        user_to_follow = get_object_or_404(CustomUser, username=username)
        user = request.user

        if Following.objects.filter(user=user, following_user=user_to_follow).exists():
            Following.objects.get(user=user, following_user=user_to_follow).delete()
            user.numof_following -= 1
            user_to_follow.numof_followers -= 1
            followed = False
        else:
            Following.objects.create(user=user, following_user=user_to_follow)
            user.numof_following += 1
            user_to_follow.numof_followers += 1
            followed = True

        user.save()
        user_to_follow.save()

        return JsonResponse({"followed":followed, "followers_count":user_to_follow.numof_followers})
    return redirect("user_profile", username=username)

@login_required
def direct(request, username):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        reciever = CustomUser.objects.get(username=username)
        sender = request.user
        if request.method == "POST":
            new_message = request.POST.get("message")
            add_message = Messages.objects.create(sender=sender, reciever=reciever, message=new_message)
            add_message.save()
        
        messages = Messages.objects.filter(reciever=reciever, sender=sender) | Messages.objects.filter(reciever=sender, sender=reciever)
        messages_list = [
            {
                "m-sender": message.sender.username,
                "m-reciever":message.reciever.username,
                "message":message.message,
            }
            for message in messages
        ]
        return JsonResponse(messages_list, safe=False)
    else:
        reciever = CustomUser.objects.get(username=username)
        sender = request.user
        if request.method == "POST":
            message = request.POST.get("message")
            add_message = Messages.objects.create(sender=sender, reciever=reciever, message=message)
            add_message.save()
        messages = Messages.objects.filter(reciever=reciever, sender=sender) | Messages.objects.filter(reciever=sender, sender=reciever)
        messages_list = [
            {
                "m-sender": message.sender.username,
                "m-reciever":message.reciever.username,
                "message":message.message,
            }
            for message in messages
        ]
        messages_dict = {"m_list":messages_list, "ajax_reciever":reciever, "ajax_sender":sender}
        return render(request, "direct.html", messages_dict)  
    


