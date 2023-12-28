from django.contrib.sitemaps import Sitemap
from .models import Post
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
 
def items(self):
    return Post.published.all()

def lastmod(self, obj):
    return obj.updated

#You can read more about the sites framework at https://docs.djangoproject.com/en/4.1/ref/contrib/sites/.
