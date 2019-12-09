from django.db import models

from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete='CASCADE') #linking an author to a superuser
    title = models.CharField(max_length = 256)
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null=True) #you can leave it blank

    def publish(self):
        self.published_date = timezone.now() #when you hit publish it will automatically enter in the date and time
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comments = True)

    def get_absolute_url(self): # must be get_absolute_url b/c that is what django looks for
        return reverse("post_detail", kwargs={'pk':self.pk}) # After a post is created go to it's detail page

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.post', related_name = 'comments', on_delete='CASCADE')
    author = models.CharField(max_length=256) # allows anyone to write their own name for a comment
    text = models.TextField(max_length=1000) # Don't wants comments to be of infinite length
    created_date = models.DateTimeField(default=timezone.now())
    approved_comments = models.BooleanField(default=False) #Must match what is above

    def approve(self):
        self.approve_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list') #A list view (homepage of all the posts on this site)

    def __str__(self):
        return self.text
