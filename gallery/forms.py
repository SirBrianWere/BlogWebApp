from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Comment

#User Sign up Form
class CustomUserCreationForm(UserCreationForm):
    email= forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username","email","password1","password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user   


#Blog Post Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        if self.user:
            instance.author = self.user
        if commit:
            instance.save()
        return instance
    
#Comment Section Form
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label = '',
        widget = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Write your comment here...'
        })
    )

    class Meta:
        model = Comment
        fields = ['content']