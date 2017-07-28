# -*- coding: utf-8 -*- vim:fileencoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

# Copyright © 2010-2012 Greek Research and Technology Network (GRNET S.A.)
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHORS DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.

## EDIT HERE
_maint_mode = False

import os
import sys
parent_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir))

if _maint_mode:

    ## EDIT THIS IF USING A CUSTOM MAINTENANCE PAGE
    _maint_file = parent_path + '/servermon/static/maintenance.html'

    with open(_maint_file, 'r') as f:
        _response_body = f.read()
        _response_len = str(len(_response_body))

    def application(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html'),
                                   ('Content-Length', _response_len)])
        yield _response_body

else:

    if parent_path not in sys.path:
        sys.path.append(parent_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servermon.settings')

    try:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
    except ImportError:
        import django.core.handlers.wsgi
        application = django.core.handlers.wsgi.WSGIHandler()

## * A version of the maintenance page display code (which allows the page to
##   be dynamically updatable) is shown commented below, but some servers in
##   secure mode will not allow application() to access local files (at least
##   without a non-trivial amount of extra code), so it is not the default. Try
##   it though if you will operate with lowered security or want to add extra
##   code to work around FS-access limitations.
#
#if _maint_mode:
#
#    ## EDIT THIS IF USING A CUSTOM MAINTENANCE PAGE
#    _maint_file = parent_path + '/servermon/static/maintenance.html'
#
#    _mtime = 0
#    _new_mtime = 0
#    _response_body = ""
#    _response_len = 0
#    _is_win = (sys.platform == "win32")
#
#    def _get_mtime():
#        global _new_mtime, _maint_file, _is_win
#        stat = os.stat(_maint_file)
#        if _is_win:
#            _new_mtime = stat.st_mtime - stat.st_ctime
#        else:
#            _new_mtime = stat.st_mtime
#
#    def _get_contents():
#        global _response_body, _response_len, _maint_file
#        with open(_maint_file, 'r') as f:
#            _response_body = f.read()
#            _response_len = str(len(_response_body))
#
#    def application(environ, start_response):
#        global _mtime, _new_mtime, _response_len, _response_body
#        _get_mtime()
#        if _mtime != _new_mtime:
#            _get_contents()
#            _mtime = _new_mtime
#        start_response('200 OK', [('Content-Type', 'text/html'),
#                                   ('Content-Length', _response_len)])
#        yield _response_body
#
#    _get_mtime()
#    _mtime = _new_mtime
#
#else:
#
#    ...
