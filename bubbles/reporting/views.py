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
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.db.models import Q

from bubbles.inventory import get_item_size_map, get_size_breakdown, get_items_in_state
from bubbles.inventory.models import Item


def index(request):
    context = {
        "title": _("Reporting"),
    }
    return render(request, "reporting/index.html", context)


def equipment_size(request):
    state_filter = ~Q(state=Item.CONDEMNED)
    item_types = get_item_size_map(state_filter).keys()
    size_count = get_size_breakdown("BCD", state_filter)
    context = {
        "title": _("Size Breakdown"),
        "item_types": item_types,
        "item": "BCD",
        "result": size_count,
    }
    return render(request, "reporting/equipment_size.html", context)


def equipment_under_repair(request):
    result = get_items_in_state(Item.REPAIR)
    context = {
        "title": _("Equipment Under Repair"),
        "result": result,
    }
    return render(request, "reporting/equipment_size.html", context)
