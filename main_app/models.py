from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Post(models.Model):
    post_title = models.CharField(max_length=100,null=True)
    post_content = models.TextField(blank=True)
    post_image = CloudinaryField('image', blank=True, null=True)  
    post_date = models.DateField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.post_content

class Reply(models.Model):
    reply_content =  models.TextField(blank=True)
    reply_image = CloudinaryField('image', blank=True, null=True)  
    reply_date = models.DateField(auto_now=True)
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        db_table = 'reply'
    
    def __str__(self):
        return self.reply_content

    @property
    def like_count(self):
        return self.like_reply.count()
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='like_reply')

    class Meta:
        db_table = 'like_table'

    def __str__(self):
        return f'{self.user}, {self.reply}'
