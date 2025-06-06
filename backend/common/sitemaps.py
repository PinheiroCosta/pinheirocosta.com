from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from .models import AboutMe


class AboutMeSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.6

    def items(self):
        return AboutMe.objects.all()[:1]

    def location(self, obj):
        return "/sobre/"

    def lastmod(self, obj):
        return obj.last_modified


class StaticPrivacySitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.3

    def items(self):
        return ["/privacidade/"]

    def location(self, item):
        return item

    def lastmod(self, item):
        return timezone.now()

