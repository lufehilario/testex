# twitter/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Post, Relationship, Like
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm, UserUpdateForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction

@login_required
def home(request):
    posts = Post.objects.all().order_by('-timestamp')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Tweet publicado com sucesso!")
            return redirect("home")
    else:
        form = PostForm()

    comment_form = CommentForm()
    context = {"posts": posts, "form": form, "comment_form": comment_form}
    return render(request, "twitter/newsfeed.html", context)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, "Conta criada com sucesso! Você já pode fazer login.")
                return redirect("login")
            except IntegrityError:
                form.add_error(None, "Ocorreu um erro ao criar a conta. Por favor, tente novamente.")
    else:
        form = UserRegisterForm()

    context = {"form": form}
    return render(request, "twitter/register.html", context)

@login_required
def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    messages.success(request, "Tweet deletado com sucesso!")
    return redirect("home")

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all().order_by('-timestamp')
    user_profile = get_object_or_404(Profile, user=user)
    is_following = False
    if request.user.is_authenticated:
        is_following = Relationship.objects.filter(from_user=request.user, to_user=user).exists()
    followers_count = Relationship.objects.filter(to_user=user).count()
    following_count = Relationship.objects.filter(from_user=user).count()
    context = {
        "user_profile": user,
        "profile": user_profile,
        "posts": posts,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count
    }
    return render(request, "twitter/profile.html", context)

@login_required
def editar(request):
    user = request.user
    user_profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Seu perfil foi atualizado com sucesso!")
            return redirect("editar")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user_profile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "twitter/editar.html", context)

@login_required
def follow(request, username):
    current_user = request.user
    to_user = get_object_or_404(User, username=username)

    # Verifica se o usuário está tentando seguir a si mesmo
    if current_user == to_user:
        messages.warning(request, "Você não pode seguir a si mesmo.")
        return redirect("profile", username=username)

    # Verifica se o usuário já está seguindo o outro usuário
    if Relationship.objects.filter(from_user=current_user, to_user=to_user).exists():
        messages.warning(request, f"Você já está seguindo {to_user.username}.")
    else:
        # Cria o relacionamento de seguir
        Relationship.objects.create(from_user=current_user, to_user=to_user)
        messages.success(request, f"Você está seguindo {to_user.username}.")

    return redirect("profile", username=username)

@login_required
def unfollow(request, username):
    current_user = request.user
    to_user = get_object_or_404(User, username=username)

    # Verifica se o usuário está tentando parar de seguir a si mesmo
    if current_user == to_user:
        messages.warning(request, "Você não pode parar de seguir a si mesmo.")
        return redirect("profile", username=username)

    # Verifica se o usuário está seguindo o outro usuário
    if Relationship.objects.filter(from_user=current_user, to_user=to_user).exists():
        # Remove o relacionamento de seguir
        Relationship.objects.filter(from_user=current_user, to_user=to_user).delete()
        messages.success(request, f"Você deixou de seguir {to_user.username}.")
    else:
        messages.warning(request, f"Você não está seguindo {to_user.username}.")

    return redirect("profile", username=username)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comentário adicionado com sucesso!")
            return redirect('home')
    else:
        form = CommentForm()

    context = {"form": form, "post": post}
    return render(request, "twitter/add_comment.html", context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        messages.success(request, "Você descurtiu o tweet.")
    else:
        messages.success(request, "Você curtiu o tweet.")
    return redirect('home')

def custom_404(request, exception):
    return render(request, 'twitter/404.html', status=404)