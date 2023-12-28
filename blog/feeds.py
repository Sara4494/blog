import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('post_list')
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish

"""

In the preceding code, we have defined a feed by subclassing the Feed class of the syndication
framework. The title, link, and description attributes correspond to the <title>, <link>, and
<description> RSS elements, respectively.
We use reverse_lazy() to generate the URL for the link attribute. The reverse() method allows you
to build URLs by their name and pass optional parameters. We used reverse() in Chapter 2, Enhancing
Your Blog with Advanced Features.
 
The reverse_lazy() utility function is a lazily evaluated version of reverse(). It allows you to use a
URL reversal before the project’s URL configuration is loaded.
The items() method retrieves the objects to be included in the feed. We retrieve the last five published
posts to include them in the feed.
The item_title(), item_description(), and item_pubdate() methods will receive each object returned by items() and return the title, description and publication date for each item.
In the item_description() method, we use the markdown() function to convert Markdown content
to HTML and the truncatewords_html() template filter function to cut the description of posts after
30 words, avoiding unclosed HTML tags

"""