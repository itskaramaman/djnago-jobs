from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group

from .forms import RegisterationForm, PostForm
from .models import Post


def home(request):
    posts = Post.objects.all()
    return render(request, 'main/home.html', {'posts': posts})


@login_required(login_url='/login')
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm()

    return render(request, 'main/post.html',
                  {'form': form, 'title': 'Create Post'})


@login_required(login_url='/login')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.data.get('title')
            post.description = form.data.get('description')
            post.save()
            return redirect('/')
    else:
        form = PostForm(instance=post)

    return render(request, 'main/post.html',
                  {'form': form, 'title': 'Update Post'})


@login_required(login_url='/login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user or request.user.has_perm('main.delete_post'):
        post.delete()
    return redirect('/home')


@login_required(login_url='/login')
def ban_user(request, ban_user_pk):
    user = get_object_or_404(User, pk=ban_user_pk)
    if request.user.is_staff:
        group = Group.objects.filter(name="default").first()
        group.user_set.remove(user)
        group = Group.objects.filter(name="mod").first()
        group.user_set.remove(user)

    return redirect('/home')


def sign_up(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home/')
    else:
        form = RegisterationForm()

    return render(request, 'registration/sign_up.html', {'form': form})
