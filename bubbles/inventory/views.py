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
from django.http import FileResponse, Http404
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.forms import formset_factory

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm

from . import models
from .models import Item, ItemValue
from .forms import InventoryCheckForm, BaseInventoryCheckFormSet

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
PAGE_INFO = _("Stock take of equipment")


def first_page(canvas, doc):
    title = _("Insurance Stock Take {}").format(
        datetime.date.today().strftime("%d %B %Y")
    )
    canvas.saveState()
    canvas.setTitle(title)
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 108, title)
    canvas.setFont("Helvetica", 12)
    canvas.drawString(cm, 0.75 * cm, _("Page 1 / {:s}").format(PAGE_INFO))
    canvas.restoreState()


def later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 12)
    canvas.drawString(cm, 0.75 * cm, _("Page {:d} {:s}").format(doc.page, PAGE_INFO))
    canvas.restoreState()


@staff_member_required
def insurance_report(request):
    path = "stock_" + datetime.date.today().strftime("%Y-%M-%d") + ".pdf"
    doc = SimpleDocTemplate(path)
    story = [Spacer(1, 2 * cm)]

    item_set = (
        Item.objects.exclude(state=Item.MISSING)
        .exclude(state=Item.CONDEMNED)
        .values("description")
        .annotate(num=Count("description"))
    )
    value_set = ItemValue.objects.all()
    table_data = [[_("Item type"), _("Quantity"), _("Unit Cost"), _("Total Cost")]]
    total_cost = 0
    for item in item_set:
        description = item["description"]
        try:
            unit_value = value_set.get(description=description).cost
        except ObjectDoesNotExist:
            unit_value = 0
        total_unit_cost = unit_value * item["num"]
        table_data += [
            [
                description,
                item["num"],
                f"R{unit_value:,d}".replace(",", " "),
                f"R{total_unit_cost:,d}".replace(",", " "),
            ]
        ]
        total_cost += total_unit_cost
    table_data += [["", "", "Total cost", f"R{total_cost:,d}".replace(",", " ")]]
    table = Table(
        table_data,
        style=[
            ("FONT", (0, 0), (len(table_data[0]) - 1, 0), "Helvetica-Bold"),
            (
                "FONT",
                (0, 1),
                (len(table_data[1]) - 1, len(table_data) - 1),
                "Helvetica",
            ),
        ],
    )
    story.append(table)
    story.append(Spacer(1, 0.2 * cm))
    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    response = FileResponse(
        open(path, "rb"),
        content_type="application/pdf",
    )
    response["Content-Disposition"] = 'filename="' + _("Insurance Inventory") + "\"'"
    return response


def expected_found(value, state):
    if state == Item.AVAILABLE or state == Item.BROKEN:
        return not value
    elif state == Item.IN_USE or state == Item.REPAIR or state == Item.MISSING:
        return value


@staff_member_required
def do_inventory_check(request, item_type):
    if item_type.lower() == "bcd":
        item_type = item_type.upper()
    else:
        item_type = item_type.title()
    try:
        item_type_class = getattr(models, item_type)
    except AttributeError:
        raise Http404("Item type does not exist")
    InventoryCheckFormSet = formset_factory(
        InventoryCheckForm,
        extra=len(Item.STATE_CHOICES),
        formset=BaseInventoryCheckFormSet,
    )
    if request.method == "POST":
        formset = InventoryCheckFormSet(
            data=request.POST,
            form_kwargs={
                "item_type": item_type_class,
            },
        )
        formset.item_type = item_type
        if formset.is_valid():
            state_transition = {
                Item.AVAILABLE: Item.MISSING,
                Item.IN_USE: Item.AVAILABLE,
                Item.BROKEN: Item.REPAIR,
                Item.REPAIR: Item.AVAILABLE,
                Item.MISSING: Item.AVAILABLE,
            }
            changed = {}
            counter = 0
            for form in formset:
                current_state = Item.STATE_CHOICES[counter][0]
                manager = item_type_class.objects
                if item_type_class == Item:
                    manager = item_type_class.item_objects
                items = list(manager.filter(state=current_state).order_by("number"))
                for item in items:
                    try:
                        data = form[item.id].data
                    except (KeyError, TypeError):
                        # Handle the case when the item is unselected, and not
                        # in the form
                        data = False
                    if expected_found(data, current_state):
                        try:
                            changed[current_state].append(item)
                        except KeyError:
                            changed[current_state] = [
                                item,
                            ]
                        item.state = state_transition[current_state]
                        item.save()
                counter += 1
            context = {
                "changed": changed,
                "state_names": Item.STATE_MAP,
                "state_transition": state_transition,
            }
            return render(request, "inventory/inventory_check_results.html", context)
    else:
        formset = InventoryCheckFormSet(
            form_kwargs={
                "item_type": item_type_class,
            }
        )
        formset.item_type = item_type
    context = {"formset": formset}
    return render(request, "inventory/inventory_check.html", context)
