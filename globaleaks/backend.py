# -*- coding: UTF-8
#   backend
#   *******
# Here is the logic for creating a twisted service. In this part of the code we
# do all the necessary high level wiring to make everything work together.
# Specifically we create the cyclone web.Application from the API specification,
# we create a TCPServer for it and setup logging.
# We also set to kill the threadpool (the one used by Storm) when the
# application shuts down.

from twisted.application.service import Application
from twisted.application import internet
from cyclone import web

from StringIO import StringIO
from globaleaks.security import GLSecureTemporaryFile

from globaleaks.utils.utility import randbits
from globaleaks.settings import GLSetting
from globaleaks.rest import api

application = Application('GLBackend')

def get_content_buffer(self, headers):
    # we always use secure temporary files in case of large json or file uploads
    if self.content_length < 100000 and headers.get("Content-Disposition") is None:
        return StringIO('')
    return GLSecureTemporaryFile(GLSetting.tmp_upload_path)

settings = dict(cookie_secret=randbits(128),
                xsrf_cookies=True,
                debug=GLSetting.http_log,
                form_urlencoded_maximum_size=GLSetting.www_form_urlencoded_maximum_size,
                no_multipart=True,
                get_content_buffer=get_content_buffer
                )

# Initialize the web API event listener, handling all the synchronous operations
GLBackendAPIFactory = web.Application(api.spec, **settings)

for ip in GLSetting.bind_addresses:
    GLBackendAPI = internet.TCPServer(GLSetting.bind_port, GLBackendAPIFactory, interface=ip)
    GLBackendAPI.setServiceParent(application)

# define exit behaviour
