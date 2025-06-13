from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .forms import *
from .forms import UserProfileForm

User = get_user_model()

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'There was an error updating your profile.')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'blog/edit_profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('post_list')

@login_required
def post_list(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.all().order_by('-published_date')

    tag_filter = request.GET.get('tag')
    if tag_filter:
        posts = posts.filter(tags__id=tag_filter)


    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'form': form  
    })


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)  
    comments = post.comments.filter(parent__isnull=True).order_by('-created_at')  
    categories = Category.objects.all() 
    post.tags.all

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return redirect('login')  

        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')  
            comment = form.save(commit=False)
            comment.post = post  
            comment.user = request.user  

            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment  
                except Comment.DoesNotExist:
                    parent_comment = None  

            comment.save()
            return redirect('post_detail', slug=slug)  
    else:
        form = CommentForm()  
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'categories': categories,  
        'tag':Tag
    })

@login_required
def post_new(request):
    author = request.user

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author
            post.save()
            
            
            selected_tags = form.cleaned_data['tags']
            post.tags.set(selected_tags)

            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()

    return render(request, 'blog/post_new.html', {'form': form})

@login_required
def post_edit(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)  
            post.save()
            form.save_m2m()  
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

    


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("post_list")
        else:
            messages.error(request, "There was an error with your signup form.")
    else:
        form = RegistrationForm()

    return render(request, 'blog/signup.html', {'form': form})

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('post_list')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

    return render(request, 'blog/login.html')

def category(request, slug):
    
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)  

    return render(request, 'blog/post_detail.html', {
        'category': category,
        'posts': posts,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.all()  
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})

# def tag(request, slug):
#     tag = get_object_or_404(Tag,slug=slug) 
#     posts = Post.objects.filter(tags=tag)  
#     context = {'tags': tag, 'posts': posts}
#     return render(request, 'blog/tags.html', context)

# def tag_posts(request, slug):
#     tag = get_object_or_404(Tag, slug=slug)  
#     posts = Post.objects.filter(tags=tag)  
#     context = {
#         'tags': tag,
#         'posts': posts
#     }
#     return render(request, 'blog/tags.html', context) 