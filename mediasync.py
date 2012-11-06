import base64
import hashlib
import mimetypes
import os
import threading

from boto.s3.key import Key
from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage

STATIC_LOCAL = getattr(settings, 'STATIC_LOCAL', settings.DEBUG)

_threadlocals = threading.local()


def checksum(data):
    pos = data.tell()
    data.seek(0)
    checksum = hashlib.md5(data.read())
    hexdigest = checksum.hexdigest()
    b64digest = base64.b64encode(checksum.digest())
    data.seek(pos)
    return (hexdigest, b64digest)


class MediaSyncMiddleware(object):

    def process_request(self, request):
        enc = request.META.get('HTTP_ACCEPT_ENCODING', '')
        _threadlocals.client_supports_gzip = 'gzip' in enc


class MediaSyncStorage(S3BotoStorage):

    def _get_key(self, name):

        name = self._encode_name(name)

        k = self.bucket.get_key(name)
        if not k:
            k = self.bucket.new_key(name)
        return k

    def _save(self, name, content):

        cleaned_name = self._clean_name(name)
        content.name = cleaned_name
        name = self._normalize_name(cleaned_name)

        content_type = getattr(content, 'content_type', mimetypes.guess_type(name)[0] or Key.DefaultContentType)

        headers = self.headers.copy()
        headers['Content-Type'] = content_type

        # sync normal file

        k = self._get_key(name)
        k.set_contents_from_file(content, headers=headers, policy=self.acl,
            reduced_redundancy=self.reduced_redundancy, rewind=True)

        # sync gzipped file

        if self.gzip and content_type in self.gzip_content_types:

            content = self._compress_content(content)
            headers['Content-Encoding'] = 'gzip'
            headers["Content-Disposition"] = 'inline; filename="%sgz"' % name.split('/')[-1]

            k = self._get_key('%s.gz' % name)
            k.set_contents_from_file(content, headers=headers, policy=self.acl,
                reduced_redundancy=self.reduced_redundancy, rewind=True)

        return cleaned_name

    def url(self, name):

        if STATIC_LOCAL:
            return os.path.join(settings.STATIC_URL, name)

        name = self._normalize_name(self._clean_name(name))
        content_type = mimetypes.guess_type(name)[0] or Key.DefaultContentType

        if self.gzip and content_type in self.gzip_content_types:
            if _threadlocals.client_supports_gzip:
                name = '%s.gz' % name

        if self.custom_domain:
            return "%s://%s/%s" % ('https' if self.secure_urls else 'http', self.custom_domain, name)
        else:
            return self.connection.generate_url(self.querystring_expire, method='GET', \
                bucket=self.bucket.name, key=self._encode_name(name), query_auth=self.querystring_auth, \
                force_http=not self.secure_urls)


class CachedMediaSyncStorage(MediaSyncStorage):
    """
    S3 storage backend that also saves files locally.
    """
    def __init__(self, *args, **kwargs):
        super(CachedMediaSyncStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "django.contrib.staticfiles.storage.StaticFilesStorage")()

    def save(self, name, content):
        self.local_storage._save(name, content)
        name = super(CachedMediaSyncStorage, self).save(name, content)
        return name
