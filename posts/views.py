from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Like, Comment, CustomUser, Follower, Story, StoryView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Exists, OuterRef
from django.contrib import messages


# 🏠 Home
@login_required
def home_view(request):
    likes = Like.objects.filter(user=request.user, post=OuterRef('pk'), status=True)
    posts = Post.objects.all().order_by('-created_at').annotate(is_liked=Exists(likes))

    cutoff_time = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(created_at__gte=cutoff_time)

    return render(request, 'home.html', {
        'posts': posts,
        'stories': stories
    })

# ❤️ Postni like qilish
@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if like.status:
        like.status = False
    else:
        like.status = True
    like.save()

    return redirect('home')


# ❤️ Like ko‘rish
@login_required
def like_view(request):
    liked_posts = Post.objects.filter(likes__user=request.user, likes__status=True).distinct()
    for post in liked_posts:
        post.is_liked = True
    return render(request, 'like.html', {'posts': liked_posts})


# ➕ Post qo‘shish
@login_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        videos = request.FILES.get('videos')
        location = request.POST.get('location')

        Post.objects.create(
            title=title,
            image=image,    
            videos=videos,
            location=location,
            user=request.user
        )
        return redirect('home')
    return render(request, 'create_post.html')


# 👤 Profil
@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(CustomUser, id=user_id)
    user_posts = Post.objects.filter(user=user_profile)

    followers_count = Follower.objects.filter(kumir=user_profile).count()
    following_count = Follower.objects.filter(fanat=user_profile).count()
    follow = Follower.objects.filter(fanat=request.user, kumir=user_profile).exists()

    yesterday = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(
        user=user_profile,
        created_at__gte=yesterday
    ).order_by('-created_at')

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'user_posts': user_posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'follow': follow,
        'stories': stories
    })


# 💬 Komment qo‘shish
@login_required
def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, user=request.user, content=text)
    return redirect('home')


@login_required
def following_add(request, user_id):
    kumir = get_object_or_404(CustomUser, id=user_id)
    fanat = request.user
    follow, created = Follower.objects.get_or_create(kumir=kumir, fanat=fanat)

    if not created:
        follow.delete()
    return redirect('profile', username=kumir.username)


@login_required
def followers_list(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    followers = Follower.objects.filter(kumir=user)  # kim uni kuzatyapti
    return render(request, 'followers.html', {
        'profile_user': user,
        'followers': followers
    })


# FOLLOWING LIST
@login_required
def following_list(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    following = Follower.objects.filter(kumir=user)  # u kimlarni kuzatyapti
    return render(request, 'following.html', {
        'profile_user': user,
        'following': following
    })


# 📖 Story qo‘shish
@login_required
def add_story(request):
    if request.method == "POST":
        media = request.FILES.get('media')
        caption = request.POST.get('caption') 
        if media:
            Story.objects.create(user=request.user, media=media, caption=caption)
            return redirect('profile', username=request.user.username)
    return render(request, "story.html")


# 👀 Story ko‘rish
@login_required
def view_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if story.created_at < timezone.now() - timedelta(hours=24):
        return redirect('profile', username=story.user.username)

    is_video = story.media.url.lower().endswith(".mp4")

    StoryView.objects.get_or_create(story=story, viewer=request.user)
    viewers = story.storyview_set.select_related("viewer")

    return render(request, 'story_detail.html', {
        'story': story,
        'is_video': is_video,
        'viewers': viewers,
        'view_count': viewers.count()
    })


# 🎥 Mening videolarim
@login_required
def my_videos(request, id):
    posts = Post.objects.filter(user__id=id, videos__isnull=False)
    return render(request, 'my_medias.html', {'posts': posts})


# 🗑️ Postni o‘chirish
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('my_videos', id=request.user.id)

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone_number = request.POST.get("phone_number")

        avatar = request.FILES.get("avatar")
        if avatar:
            user.avatar = avatar

        user.save()
        return redirect("profile", request.user.id) 

    return render(request, "edit_profile.html", {"user": user})