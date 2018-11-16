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
import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import FileResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm

from .models import Item, ItemValue

PAGE_HEIGHT = defaultPageSize[1];
PAGE_WIDTH = defaultPageSize[0]
PAGE_INFO = _('Stock take of equipment')

def first_page(canvas, doc):
    title = _('Insurance Stock Take {}').format(datetime.date.today().strftime('%d %B %Y'))
    canvas.saveState()
    canvas.setTitle(title)
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 108, title)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(cm, 0.75 * cm,
                      _('Page 1 / {:s}').format(PAGE_INFO))
    canvas.restoreState()

def later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 12)
    canvas.drawString(cm, 0.75 * cm,
                      _('Page {:d} {:s}').format(doc.page, PAGE_INFO))
    canvas.restoreState()

@staff_member_required
def insurance_report(request):
    styles = getSampleStyleSheet()
    path = 'stock_' + datetime.date.today().strftime('%Y-%M-%d') + '.pdf'
    doc = SimpleDocTemplate(path)
    story = [Spacer(1, 2 * cm)]
    style = styles['Normal']

    item_set = Item.objects.exclude(state=Item.MISSING, state=Item.CONDEMNED).values('description').annotate(num=Count('description'))
    value_set = ItemValue.objects.all()
    table_data = [[_('Item type'), _('Quantity'), _('Unit Cost'), _('Total Cost')]]
    total_cost = 0
    for item in item_set:
        description = item['description']
        try :
            unit_value = value_set.get(description=description).cost
        except ObjectDoesNotExist:
            unit_value = 0
        total_unit_cost = unit_value * item['num']
        table_data += [[description, item['num'],
                        'R{:,d}'.format(unit_value).replace(',', ' '),
                        'R{:,d}'.format(total_unit_cost).replace(',', ' ')]]
        total_cost += total_unit_cost
    table_data += [['', '', 'Total cost',
                    'R{:,d}'.format(total_cost).replace(',', ' ')]]
    table = Table(table_data, style=
                  [('FONT', (0,0), (len(table_data[0]) - 1, 0), 'Helvetica-Bold'),
                  ('FONT', (0, 1), (len(table_data[1]) - 1, len(table_data) - 1),
                   'Helvetica'),])
    story.append(table)
    story.append(Spacer(1, 0.2 * cm))
    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    response = FileResponse(open(path, 'rb'), content_type='application/pdf', )
    response['Content-Disposition'] = 'filename="' + _('Insurance Inventory') + '"\''
    return response
