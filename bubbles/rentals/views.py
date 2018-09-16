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

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldDoesNotExist
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from bubbles.inventory.models import Item, BCD, Booties, Cylinder, Fins, Wetsuit
from .models import Rental, RequestItem, RentalPeriod, RentalItem
from .forms import RequestEquipmentForm, RentEquipmentForm, ReturnEquipmentForm

@login_required
def index(request):
    rental_set = Rental.objects.filter(user=request.user,
                                       state=Rental.RENTED)

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
                rental_item.rental = rental
                rental_item.save()
            return render(request, 'rentals/request_confirmation.html')
    else:
        form = RequestEquipmentForm(user=request.user)

    context = {
        'form': form,
        'url': reverse('rentals:request_equipment'),
        'title': _('Request Equipment'),
        'show_cost': False,
    }

    return render(request, 'rentals/rent_equipment.html', context)

@login_required
def rent_equipment(request, rental_request=None):
    if not request.user.is_staff:
        return redirect('rentals:request_equipment')

    url = reverse('rentals:rent_equipment')
    if request.method == 'POST':
        try:
            rental = Rental.objects.get(id=rental_request)
            user = rental.user
        except Rental.DoesNotExist:
            rental = None
            user = request.user
        form = RentEquipmentForm(user=user, rental=rental, data=request.POST)
        if (rental_request):
            url = reverse('rentals:rent_equipment', args=(rental_request,))
        else:
            url = reverse('rentals:rent_equipment')
        if form.is_valid():
            period = form.cleaned_data['period']
            period.save()
            rental = form.rental
            rental.rental_period = period
            rental.state = Rental.RENTED
            rental.approved_by = request.user
            rental.save()
            for rental_item in form.cleaned_data['equipment']:
                rental_item.item.state = Item.IN_USE
                rental_item.item.save()
                rental_item.save()
            RequestItem.objects.filter(rental=rental).delete()
            return render(request, 'rentals/rental_confirmation.html')
    else:
        if rental_request:
            rental = Rental.objects.get(id=rental_request)
            url = reverse('rentals:rent_equipment', args=(rental_request,))
            form = RentEquipmentForm(user=rental.user,
                                     rental=rental,
                                     data={
                                         'equipment': rental.requestitem_set.all(),
                                         'period': rental.rental_period,
                                         'deposit': rental.deposit,
                                     })
        else:
            form = RentEquipmentForm(user=request.user)
    context = {
        'form': form,
        'url': url,
        'rental_user': form.user,
        'title': _('Rent Equipment'),
        'show_cost': True,
    }

    return render(request, 'rentals/rent_equipment.html', context)

@login_required
def return_equipment(request, rental):
    if not request.user.is_staff:
        return redirect('rentals:request_equipment')

    url = reverse('rentals:rent_equipment')
    if request.method == 'POST':
        rental = Rental.objects.get(id=rental)
        form = ReturnEquipmentForm(user=request.user, rental=rental, data=request.POST)
        url = reverse('rentals:return_equipment', args=(rental.id,))
        if form.is_valid():
            rental = form.rental
            rental.state = Rental.RETURNED
            rental.approved_by = request.user
            rental.save()
            if rental.rental_period.end_date == None:
                rental.rental_period.end_date = datetime.date.today()
                retnal.rental_period.save()
            for rental_item in form.cleaned_data['equipment']:
                rental_item.item.state = Item.AVAILABLE
                rental_item.item.save()
                rental_item.save()
            return render(request, 'rentals/return_confirmation.html')
    else:
        rental = Rental.objects.get(id=rental)
        url = reverse('rentals:return_equipment', args=(rental.id,))
        form = ReturnEquipmentForm(user=rental.user,
                                   rental=rental,
                                   data={
                                     'equipment': rental.rentalitem_set.all(),
                                     'deposit': rental.deposit,
                                   })

    context = {
        'form': form,
        'url': url,
        'rental_user': form.user,
        'title': _('Return Equipment'),
        'show_cost': False,
    }
    return render(request, 'rentals/rent_equipment.html', context)
