from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Post(models.Model):
    post_content = models.CharField()
    post_image = models.ImageField(upload_to='post_images/',null=True)
    post_date = models.DateField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    class Meta:
        db_table = 'post'

    def __str__(self):
        return self.post_content

class Reply(models.Model):
    reply_content = models.CharField()
    reply_image = models.ImageField(upload_to='reply_images/',null= True)
    reply_date = models.DateField(auto_now=True)
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')

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
