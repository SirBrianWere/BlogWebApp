from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

#Defines Structure of Data

#Blog Post Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #Author Field
    likes  = models.ManyToManyField(User, related_name='blog_posts',blank=True)

    #READ
    def __str__(self):
        return self.name


    #EDIT
    def edit(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image
        self.save()

    #Blog Post Description
    def short_description(self):
        # Split the description into words
        words = self.description.split()
        if len(words) > 50:
            # Join the first 50 words and add "..." at the end
            return ' '.join(words[:30]) + '...'
        else:
            # If the description is already less than 50 words, return it as is
            return self.description
        
    #  LIKES
    @property
    def total_likes(self):
        return self.likes.count()
        
#Comment Section Model
class Comment(models.Model):
    product=models.ForeignKey(Product,  related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on "{self.post.name}"'