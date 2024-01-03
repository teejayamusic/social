# yourappname/views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout,get_user_model
from .forms import CustomUserCreationForm, CustomAuthenticationForm,ChatMessageForm,YourProfileForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like,CustomUser,Friendship,ChatMessage
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
import logging
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


CustomUser = get_user_model()





@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = YourProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = YourProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

class ProfileUpdateView(UpdateView):
    model = CustomUser
    template_name = 'edit_profile.html'
    form_class = YourProfileForm
    success_url = reverse_lazy('profile')

@login_required(login_url='/login/')
def view_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'view_profile.html', context)





















def friend_profile(request, friend_id):
    friend = get_object_or_404(CustomUser, id=friend_id)
    user=request.user
    chats=ChatMessage.objects.all()
    form = ChatMessageForm()
    if request.method=="POST":
        form=ChatMessageForm(request.POST)
        if form.is_valid():
            chat=form.save(commit=False)
            chat.sender=user
            chat.receiver=friend
            chat.save()
            return redirect('friend_profile', friend_id=friend_id)
    return render(request, 'friend_profile.html', {'friend': friend,'form':form,"user":user,'chats':chats})




def user_detail(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_posts = Post.objects.filter(user=user).order_by('-created_at')
    context = {'user': user,'user_posts':user_posts}
    
    return render(request, 'user_detail.html', context)
    

 

logger = logging.getLogger(__name__)












def all_posts(request):

    all_posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'all_posts': all_posts, 'user': request.user})
def index(request):
    

    # Get friend requests
    friend_requests = Friendship.objects.filter(to_user=request.user, is_accepted=False)

    # Get user posts
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')

    context = {
        
        'friend_requests': friend_requests,
        
    }


    indexpost = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'indexpost': indexpost, 'user': request.user})

@login_required
def friend_request(request, username):
    try:
        to_user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('home')

    logger.info(f"Processing friend request for user: {to_user.username}")

    # Check if a friendship already exists or if the request is from the current user
    if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists() or request.user == to_user:
        messages.warning(request, 'Invalid friend request.')
        logger.warning('Invalid friend request.')
        return HttpResponse('Invalid friend request.')

    # Check if a friend request has already been sent
    existing_request = Friendship.objects.filter(from_user=request.user, to_user=to_user, is_accepted=False)
    if existing_request.exists():
        messages.info(request, 'Friend request already sent.')
        logger.info('Friend request already sent.')
        return HttpResponse('Friend request already sent.')

    # Create a new friend request
    Friendship.objects.create(from_user=request.user, to_user=to_user)

    messages.success(request, f'Friend request sent to {to_user.username}.')
    logger.info(f'Friend request sent to {to_user.username}.')
    return redirect('home')



def send_friend_request(request, username):
    print(f"Sending friend request to {username}")
    
    # Existing code...

    print("Friend request sent successfully.")
    return redirect('home')



@login_required(login_url='/login/')
def home(request):
    # Get random users excluding the current user and users already in friends list
    random_users = CustomUser.objects.exclude(id=request.user.id).exclude(friends=request.user).order_by('?')[:5]

    # Get friend requests
    friend_requests = Friendship.objects.filter(to_user=request.user, is_accepted=False)

    # Get user posts
    user_posts = Post.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'random_users': random_users,
        'friend_requests': friend_requests,
        'user_posts': user_posts,
    }

    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import redirect



@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


from .forms import PostCreationForm










def accept_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user)
    friendship.accept()
    return redirect('home')



def search_users(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        users = CustomUser.objects.filter(username__icontains=query)
        return render(request, 'search_results.html', {'users': users})








@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST,request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            
            form.instance.user = request.user
            form.save()
            return redirect('home')
       
    else:
        
        form = PostCreationForm()
    return render(request, 'create_post.html', {'form': form})

def view_post(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    likes = post.likes.all()
    return render(request, 'view_post.html', {'post': post, 'comments': comments, 'likes': likes})

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post.objects.get(id=post_id)
            Comment.objects.create(user=request.user, post=post, content=content)
    return redirect('view_post', post_id=post_id)

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.create(user=request.user, post=post)
    return redirect('view_post', post_id=post_id)















































