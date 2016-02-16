# -*- coding: utf-8 -*-
'''
    sphinx_pypi_upload
    ~~~~~~~~~~~~~~~~~~

    setuptools command for uploading Sphinx documentation to PyPI

    :author: Jannis Leidel
    :contact: jannis@leidel.info
    :copyright: Copyright 2009, Jannis Leidel.
    :license: BSD, see LICENSE for details.
'''

import os
import socket
import zipfile
import base64
import tempfile
import io as StringIO

try:
    from httplib import HTTPConnection, HTTPSConnection
    from urlparse import urlparse
except ImportError:
    # Python 3
    from http.client import HTTPConnection, HTTPSConnection
    from urllib.parse import urlparse

from distutils import log
from distutils.command.upload import upload
from distutils.errors import DistutilsOptionError


class UploadDoc(upload):

    '''Distutils command to upload Sphinx documentation.'''

    description = 'Upload Sphinx documentation to PyPI'
    user_options = [
        ('repository=', 'r',
         "url of repository [default: %s]" % upload.DEFAULT_REPOSITORY),
        ('show-response', None,
         'display full response text from server'),
        ('upload-dir=', None, 'directory to upload'),
    ]
    boolean_options = upload.boolean_options

    def initialize_options(self):
        upload.initialize_options(self)
        self.upload_dir = None

    def finalize_options(self):
        upload.finalize_options(self)
        if self.upload_dir is None:
            build = self.get_finalized_command('build')
            self.upload_dir = os.path.join(build.build_base, 'sphinx')
            self.mkpath(self.upload_dir)
        self.ensure_dirname('upload_dir')
        self.announce('Using upload directory %s' % self.upload_dir)

    def create_zipfile(self):
        name = self.distribution.metadata.get_name()
        tmp_dir = tempfile.mkdtemp()
        tmp_file = os.path.join(tmp_dir, '%s.zip' % name)
        zip_file = zipfile.ZipFile(tmp_file, 'w')
        if not os.path.exists(os.path.join(self.upload_dir, 'index.html')):
            raise DistutilsOptionError(
                'index.html not found in upload directory %r'
                % self.upload_dir)
        for root, dirs, files in os.walk(self.upload_dir):
            for name in files:
                full = os.path.join(root, name)
                relative = root[len(self.upload_dir):].lstrip(os.path.sep)
                dest = os.path.join(relative, name)
                zip_file.write(full, dest)
        zip_file.close()
        return tmp_file

    def upload_file(self, filename):
        content = open(filename, 'rb').read()
        meta = self.distribution.metadata
        data = {
            ':action': b'doc_upload',
            'name': meta.get_name().encode('ascii'),
            'content': (os.path.basename(filename), content),
        }
        # set up the authentication
        auth = (self.username + ':' + self.password).encode('ascii')
        auth = b"Basic " + base64.encodestring(auth).strip()

        # Build up the MIME payload for the POST data
        boundary = b'--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'
        sep_boundary = b'\n--' + boundary
        end_boundary = sep_boundary + b'--'
        body = StringIO.BytesIO()
        for key, value in data.items():
            # handle multiple entries for the same name
            if not isinstance(value, list):
                value = [value]

            for value in value:
                if type(value) is tuple:
                    fn = (';filename="%s"' % value[0]).encode('ascii')
                    value = value[1]
                else:
                    fn = b""
                body.write(sep_boundary)
                body.write(('\nContent-Disposition: form-data; name="%s"'
                            % key).encode('ascii'))
                body.write(fn)
                body.write(b"\n\n")
                body.write(value)
                if value and value[-1] == b'\r':
                    body.write(b'\n')  # write an extra newline (lurve Macs)
        body.write(end_boundary)
        body.write(b"\n")
        body = body.getvalue()

        self.announce("Submitting documentation to %s" %
                      (self.repository), log.INFO)

        # build the Request
        # We can't use urllib2 since we need to send the Basic
        # auth right with the first request
        schema, netloc, url, params, query, fragments = \
            urlparse(self.repository)
        assert not params and not query and not fragments
        if schema == 'http':
            http = HTTPConnection(netloc)
        elif schema == 'https':
            http = HTTPSConnection(netloc)
        else:
            raise AssertionError("unsupported schema " + schema)

        data = ''
        try:
            http.connect()
            http.putrequest("POST", url)
            http.putheader('Content-type',
                           'multipart/form-data; boundary=%s' % boundary)
            http.putheader('Content-length', str(len(body)))
            http.putheader('Authorization', auth)
            http.endheaders()
            http.send(body)
        except socket.error as e:
            self.announce(str(e), log.ERROR)
            return

        response = http.getresponse()
        if response.status == 200:
            self.announce(
                'Server response (%s): %s'
                % (response.status, response.reason),
                log.INFO)
        elif response.status == 301:
            location = response.getheader('Location')
            if location is None:
                location = 'http://packages.python.org/%s/' % meta.get_name()
            self.announce('Upload successful. Visit %s' % location,
                          log.INFO)
        else:
            self.announce(
                'Upload failed (%s): %s' %
                (response.status, response.reason),
                log.ERROR)
        if self.show_response:
            print('-' * 75)
            print(response.read().strip())
            print('-' * 75)

    def run(self):
        zip_file = self.create_zipfile()
        self.upload_file(zip_file)
        os.remove(zip_file)
