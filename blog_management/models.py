from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def get_blog_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Blog(models.Model):
    BLOG_STATUS_CHOICES = (("DRAFT", "DRAFT"), ("PUBLISHED", "PUBLISHED"), ("DELETED", "DELETED"))
    title = models.CharField(max_length=150)
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to=get_blog_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=BLOG_STATUS_CHOICES)

    class Meta:
        db_table = "blog"

class BlogActivity(models.Model):
    BLOG_ACTIVITY_CHOICES = (("LIKE", "LIKE"), ("SAVE", "SAVE"), ("SHARE", "SHARE"))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=BLOG_ACTIVITY_CHOICES)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_activity"

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_pinned = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comment"

class CommentReplies(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    like_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comment_replies"