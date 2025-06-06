from django.contrib.sitemaps import Sitemap
from .models import Tool


class ToolSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Tool.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.created_at

