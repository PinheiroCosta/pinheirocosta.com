from django.core.files.storage import default_storage


IMAGE_MIME_PREFIX = "image/"
VIDEO_MIME_PREFIX = "video/"

def upload_blog_media(file):
    content_type = file.content_type or ""

    if content_type.startswith(IMAGE_MIME_PREFIX):
        base_path = "blog/images"
    elif content_type.startswith(VIDEO_MIME_PREFIX):
        base_path = "blog/videos"
    else:
        raise ValueError("Tipo de mídia não suportado")

    path = default_storage.save(f"{base_path}/{file.name}", file)
    return default_storage.url(path)
