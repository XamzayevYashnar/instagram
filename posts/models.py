from django.db import models
from users.models import CustomUser
from config import settings

class Post(models.Model):
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    videos = models.FileField(upload_to='post_videos/', null=True, blank=True)  # Tuzatildi
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    @property
    def liked_by_user(self):
        return False
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Tuzatildi

    def __str__(self) -> str:
        return f'Comment user: {self.user} on {self.post.title}'

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')  # Tuzatildi
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]

class Follower(models.Model):
    fanat = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fanat')
    kumir = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='kumir')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)    

class Story(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media = models.FileField(upload_to="stories/")
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Story by {self.user.username} - {self.created_at}"

    @property
    def view_count(self):
        return self.storyview_set.count()

    def has_viewed(self, user):
        return self.storyview_set.filter(viewer=user).exists()

class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['story', 'viewer'], name='unique_storyview')
        ]