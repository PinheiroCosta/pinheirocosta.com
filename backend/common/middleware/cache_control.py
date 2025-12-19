from django.utils.deprecation import MiddlewareMixin


class DefaultCacheControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if "Cache-Control" not in response and response.get(
            "Content-Type", ""
        ).startswith("text/html"):
            response["Cache-Control"] = "no-store"
        return response
