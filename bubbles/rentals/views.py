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

from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from bubbles.inventory.models import Item, BCD, Booties, Cylinder, Fins, Wetsuit
from .models import Rental


@login_required
def index(request):
    rental_set = Rental.objects.filter(user=request.user)

    context = {}
    if (len(rental_set) != 0):
        context['rentals'] = rental_set
    return render(request, 'rentals/index.html', context)

def get_sizes(item_type, size_tag='size'):
    sizes_set = item_type.objects.filter(state__exact=Item.AVAILABLE).values(size_tag).distinct()
    sizes = [i[size_tag] for i in sizes_set]
    return sizes

@login_required
def request_equipment(request):
    item_types = Item.objects.filter(state__exact=Item.AVAILABLE).values('description').distinct()
    item_size_map = {}
    item_size_map['BCD'] = get_sizes(BCD)
    item_size_map['Booties'] = get_sizes(Booties)
    item_size_map['Cylinder'] = get_sizes(Cylinder, 'capacity')
    item_size_map['Fins'] = get_sizes(Fins)
    item_size_map['Wetsuit'] = get_sizes(Wetsuit)
    context = {
        'item_types': item_types,
        'item_size_map': item_size_map,
    }
    return render(request, 'rentals/request_equipment.html', context)

@login_required
def rent_equipment(request, rental_request=None):
    if not request.user.is_staff:
        return redirect('rentals:request_equipment')
    context = {}
    if (rental_request):
        context['rental'] = Rental.objects.get(id=rental_request)
    return render(request, 'rentals/request_equipment.html', context)

