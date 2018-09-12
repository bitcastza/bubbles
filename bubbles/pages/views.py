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
import markdown

from django.http import Http404
from django.shortcuts import render
from bubbles.settings import MEDIA_ROOT

PAGE_ROOT = 'pages'

class EscapeHtml(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']

def page(request, page_name):
    filename = os.path.join(MEDIA_ROOT, PAGE_ROOT, page_name) + '.md'
    try:
        input_file = codecs.open(filename, mode="r", encoding="utf-8")
    except FileNotFoundError:
        raise Http404('Page not found')

    text = input_file.read()
    html = markdown.markdown(text, extensions=[EscapeHtml()])
    context = {'body': html}
    return render(request, 'pages/page.html', context)
