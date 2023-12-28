from django import template
from ..models import Post
from django.db.models import Count
 
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
@register.simple_tag
def total_posts():
 return Post.published.count()

@register.simple_tag
def get_most_commented_posts(count=5):
 return Post.published.annotate(
 total_comments=Count('comments')
 ).order_by('-total_comments')[:count]

@register.inclusion_tag('post/latest_posts.html')
def show_latest_posts(count=5):
 latest_posts = Post.published.order_by('-publish')[:count]
 return {'latest_posts': latest_posts}
@register.simple_tag
def get_most_commented_posts(count=5):
 return Post.published.annotate(
 total_comments=Count('comments')
 ).order_by('-total_comments')[:count]
 
@register.filter(name='markdown')
def markdown_format(text):
 return mark_safe(markdown.markdown(text))

"""
In the preceding template tag, you build a QuerySet using the annotate() function to aggregate the
total number of comments for each post. You use the Count aggregation function to store the number
of comments in the computed total_comments field for each Post object. You order the QuerySet by
the computed field in descending order. You also provide an optional count variable to limit the total
number of objects returned
"""

# https://docs.djangoproject.com/en/4.1/topics/db/aggregation/
# https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/
#You can find the list of Django’s built-in template filters at https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#built-in-filter-reference.

#You have now a clear idea about how to build custom template tags. You can read more about them at
#https://docs.djangoproject.com/en/4.1/howto/custom-template-tags/.