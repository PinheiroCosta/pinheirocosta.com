from storages.backends.s3boto3 import S3Boto3Storage


class MediaR2Storage(S3Boto3Storage):
    default_acl = None
    file_overwrite = False
