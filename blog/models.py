from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse 
from taggit.managers import TaggableManager
 
class PublishedManager(models.Manager):
 def get_queryset(self):
    return super().get_queryset()\
    .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        #We have defined the enumeration class Status by subclassing models.TextChoices. The available
        ##choices for the post status are DRAFT and PUBLISHED. Their respective values are DF and PB, and their
        #labels or readable names are Draft and Published.
        
    tags = TaggableManager()#The tags manager will allow you to add, retrieve, and remove tags from Post objects.
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    author = models.ForeignKey(User,
 on_delete=models.CASCADE,
 related_name='blog_posts')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    slug = models.SlugField(max_length=250,
 unique_for_date='publish')
    class Meta:
        ordering = ['-publish']
        #We have added a Meta class inside the model. This class defines metadata for the model. We use the
        #ordering attribute to tell Django that it should sort results by the publish field. This ordering will
        #apply by default for database queries when no specific order is provided in the query. We indicate
        #descending order by using a hyphen before the field name, -publish. Posts will be returned in reverse
        #chronological order by default.
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail',
        args=[self.publish.year,
 self.publish.month,
self.publish.day,
self.slug])
        #The reverse() function will build the URL dynamically using the URL name defined in the URL
    #patterns. We have used the blog namespace followed by a colon and the URL name post_detail.
    #Remember that the blog namespace is defined in the main urls.


class Comment(models.Model):
    post = models.ForeignKey(Post,
    on_delete=models.CASCADE,
    related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'