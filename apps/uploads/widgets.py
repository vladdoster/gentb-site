#
# Copyright (C) 2015 Adam Bogdal
#               2017 Maha Farhat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Code from: https://github.com/bogdal/django-dropboxchooser-field by Adam Bogdal.
# It is unlicensed. We're assuming Public Domain, MIT or some other permissive
# license.
#

from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms import TextInput

import json

class UploadChooserWidget(TextInput):
    input_type = 'upload-chooser'

    def __init__(self, extensions=None, attrs=None, buckets=None):
        extensions = ['.' + x.strip('.') for x in (extensions or [])]
        kw = {
            'style': 'display: none',
            'data-app-key': getattr(settings, 'DROPBOX_APP_KEY', None),
            'data-extensions': " ".join(extensions),
        }
        self.buckets = buckets or []
        kw.update(attrs or {})
        super(UploadChooserWidget, self).__init__(kw)

    def render(self, name, value, attrs):
        render = super(UploadChooserWidget, self).render
        attrs['data-resumable_url'] = reverse('uploads:resumable')
        attrs['data-manual_url'] = reverse('uploads:manual')
        ret = render(name, value, attrs)
        for bucket, match, label, link in self.buckets:
            kw = attrs.copy()
            kw['type'] = 'bucket'
            kw['data-match'] = match
            kw['data-parent'] = kw['id']
            kw['data-label'] = label
            kw['data-bucket'] = bucket
            kw['data-link'] = link
            kw['id'] += '_' + bucket
            ret += render(name + '_' + bucket, '', kw)
        return ret

    class Media:
        js = [
          # Dropbox javascript support
          'https://www.dropbox.com/static/api/2/dropins.js?cache=2',
          # Chunked file uploader support
          'js/resumable.js',
          # Bootbox used in URL Uploader
          'js/bootbox.min.js',
          # Generic uploader support (binds together the above)
          'js/uploads/chooser.js']
        css = {'all': ('css/uploads/chooser.css',)}

