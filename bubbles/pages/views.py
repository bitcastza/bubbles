###########################################################################
# Bubbles is Copyright (C) 2018 Kyle Robbertze <krobbertze@gmail.com>
#
# Bubbles is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Bubbles is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Bubbles. If not, see <http://www.gnu.org/licenses/>.
###########################################################################
import codecs
import os

from markdown import markdown, Extension
from markdown.inlinepatterns import InlineProcessor
from xml.etree import ElementTree
from django.http import Http404
from django.shortcuts import render
from django.conf import settings

PAGE_ROOT = 'pages'

class ImageClass(InlineProcessor):
    def handleMatch(self, m, data):
        img = ElementTree.Element('img')
        img.attrib['class'] = 'img-fluid rounded'
        img.attrib['alt'] = m.group(1)
        img.attrib['src'] = m.group(2)
        img.attrib['title'] = m.group(3)
        return img, m.start(0), m.end(0)

class EscapeHtml(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')
        img_pattern = ImageClass(r'!\[(.+)]\((.+) "(.+)"\)')
        md.inlinePatterns.register(img_pattern, 'img_pattern', 175)

def page(request, page_name):
    filename = os.path.join(settings.MEDIA_ROOT, PAGE_ROOT, page_name) + '.md'
    try:
        input_file = codecs.open(filename, mode="r", encoding="utf-8")
    except FileNotFoundError:
        raise Http404('Page not found')

    text = input_file.read()
    html = markdown(text, extensions=[EscapeHtml(),
                                      'markdown.extensions.attr_list'])
    context = {'body': html}
    return render(request, 'pages/page.html', context)
