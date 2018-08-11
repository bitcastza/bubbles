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
from django.urls import reverse

from bubbles.inventory.models import Item, BCD, Booties, Cylinder, Fins, Wetsuit
from .models import Rental
from .forms import RequestEquipmentForm, RentEquipmentForm


@login_required
def index(request):
    rental_set = Rental.objects.filter(user=request.user)

    context = {}
    if (len(rental_set) != 0):
        context['rentals'] = rental_set
    return render(request, 'rentals/index.html', context)

@login_required
def request_equipment(request):
    if request.method == 'POST':
        form = RequestEquipmentForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.cleaned_data['period'].save()
            rental = form.rental
            rental.state = Rental.REQUESTED
            rental.save()
            for rental_item in form.cleaned_data['equipment']:
                rental_item.item.save()
                rental_item.save()
            return render(request, 'rentals/rental_confirmation.html')
    else:
        form = RequestEquipmentForm(user=request.user)

    context = {
        'form': form,
        'url': reverse('rentals:request_equipment'),
        'title': _('Request Equipment'),
    }

    return render(request, 'rentals/rent_equipment.html', context)

@login_required
def rent_equipment(request, rental_request=None):
    if not request.user.is_staff:
        return redirect('rentals:request_equipment')

    url = reverse('rentals:rent_equipment')
    rental = Rental.objects.get(id=rental_request)
    if request.method == 'POST':
        form = RentEquipmentForm(user=request.user, rental=rental, data=request.POST)
        url = reverse('rentals:rent_equipment', args=(rental_request,))
        if form.is_valid():
            form.cleaned_data['period'].save()
            rental = form.rental
            rental.state = Rental.RENTED
            rental.approved_by = request.user
            rental.save()
            for rental_item in form.cleaned_data['equipment']:
                rental_item.item.state = Item.IN_USE
                rental_item.item.save()
                rental_item.save()
            return render(request, 'rentals/rental_confirmation.html')
    else:
        if rental_request:
            url = reverse('rentals:rent_equipment', args=(rental_request,))
            form = RentEquipmentForm(user=request.user,
                                     rental=rental,
                                     data={
                                         'equipment': rental.rentalitem_set.all(),
                                         'period': rental.rental_period,
                                         'deposit': rental.deposit,
                                     })
        else:
            form = RentEquipmentForm(user=request.user)

    context = {
        'form': form,
        'url': url,
        'title': _('Rent Equipment'),
    }

    return render(request, 'rentals/rent_equipment.html', context)
