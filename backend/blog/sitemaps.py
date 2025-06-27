from django.contrib.sitemaps import Sitemap
from .models import BlogPost


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(status=BlogPost.PUBLICADO)

    def lastmod(self, obj):
        return obj.atualizado_em
