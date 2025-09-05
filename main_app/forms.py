from django import forms
from .models import Post , Category
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['username','password']
    
    def save(self):
     user = super().save()
     user.set_password(self.cleaned_data["password"])
     user.save()
     return user

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
       queryset= Category.objects.all(),
       empty_label='Select a Category'
    )
    class Meta:
        model = Post
        fields = ['post_title','post_content','post_image','category']
       