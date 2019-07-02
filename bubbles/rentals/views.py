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

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.models import LogEntry
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from bubbles.inventory.models import Item, BCD, Booties, Cylinder, Fins, Wetsuit, Weight
from .models import Rental, RequestItem, RentalPeriod, RentalItem
from .forms import RequestEquipmentForm, RentEquipmentForm, ReturnEquipmentForm

@login_required
def index(request):
    rental_set = RentalItem.objects.filter(rental__user=request.user,
                                           returned=False)
    requests = Rental.objects.filter(user=request.user, state=Rental.REQUESTED)

    context = {}
    if (rental_set.count() != 0):
        context['rentals'] = rental_set
    if (requests.count() != 0):
        context['requests'] = requests
    return render(request, 'rentals/index.html', context)

@login_required
def request_equipment(request, request_id=None):
    url = reverse('rentals:request_equipment')
    if request.method == 'POST':
        if request_id:
            url = reverse('rentals:request_equipment', args=(request_id,))
            rental_request = get_object_or_404(Rental, id=request_id)
            form = RequestEquipmentForm(user=request.user,
                                        request_id=request_id,
                                        rental=rental_request,
                                        data=request.POST)
        else:
            form = RequestEquipmentForm(user=request.user,
                                        data=request.POST)
        if form.is_valid():
            form.cleaned_data['period'].save()
            rental = form.rental
            rental.state = Rental.REQUESTED
            rental.weight = form.cleaned_data['belt_weight']
            rental.save()
            RequestItem.objects.filter(rental=rental).delete()
            for rental_item in form.cleaned_data['equipment']:
                rental_item.rental = rental
                rental_item.save()
            return render(request, 'rentals/request_confirmation.html')
    elif request_id != None: # Edit
        rental_request = get_object_or_404(Rental, id=request_id)
        url = reverse('rentals:request_equipment', args=(request_id,))
        if rental_request.user != request.user:
            raise PermissionDenied
        form = RequestEquipmentForm(user=request.user,
                                    request_id=request_id,
                                    rental=rental_request,
                                    data={
                                        'period': rental_request.rental_period,
                                        'equipment': rental_request.requestitem_set.all(),
                                        'belt_weight': rental_request.weight,
                                        'liability': True,
                                    })
    else:
        form = RequestEquipmentForm(user=request.user)

    context = {
        'form': form,
        'url': url,
        'title': _('Request Equipment'),
        'show_cost': False,
    }

    return render(request, 'rentals/rent_equipment.html', context)

def get_existing_rentals(user):
    existing_rental = Rental.objects.filter(user=user,
                                            state=Rental.RENTED)
    if existing_rental.count() > 0:
        return existing_rental.first()
    return None


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
            # Staff member renting for themselves
            rental = get_existing_rentals(request.user)
            user = request.user
        form = RentEquipmentForm(user=user, rental=rental, data=request.POST)
        if rental_request:
            url = reverse('rentals:rent_equipment', args=(rental_request,))
        if form.is_valid():
            period = form.cleaned_data['period']
            period.save()
            rental = form.rental
            rental.rental_period = period
            rental.state = Rental.RENTED
            rental.approved_by = request.user
            num_weights = form.cleaned_data['belt_weight']
            total_weight = Weight.objects.first()
            total_weight.available_weight = total_weight.available_weight - num_weights
            total_weight.save()
            rental.weight = num_weights
            rental.save()
            for rental_item in form.cleaned_data['equipment']:
                rental_item.item.state = Item.IN_USE
                rental_item.item.save()
                rental_item.rental = rental
                rental_item.returned = False
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
                                         'belt_weight': rental.weight,
                                     })
        else:
            # Staff member renting for themselves
            rental = get_existing_rentals(request.user)
            form = RentEquipmentForm(user=request.user, rental=rental,
                                     data={
                                         'period': None,
                                         'deposit': 0,
                                         'belt_weight': 0,
                                     })
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
        form = ReturnEquipmentForm(user=rental.user, rental=rental, data=request.POST)
        url = reverse('rentals:return_equipment', args=(rental.id,))
        if form.is_valid():
            rental = form.rental
            for rental_item in form.cleaned_data['equipment']:
                rental_item.item.state = Item.AVAILABLE
                rental_item.item.save()
                rental_item.returned = True
                rental_item.save()
            all_returned = True
            for rental_item in rental.rentalitem_set.filter(returned=False):
                if rental_item not in form.cleaned_data['equipment']:
                    all_returned = False
                    break
            returned_weight = form.cleaned_data['belt_weight']
            total_weight = Weight.objects.first()
            total_weight.available_weight = total_weight.available_weight + returned_weight
            if total_weight.available_weight > total_weight.total_weight:
                total_weight.total_weight = total_weight.available_weight
            total_weight.save()
            if returned_weight != rental.weight:
                all_returned = False
            rental.approved_by = request.user
            if all_returned:
                rental.state = Rental.RETURNED
                rental.save()
                if rental.rental_period.end_date == None:
                    rental.rental_period.end_date = datetime.date.today()
                    rental.rental_period.save()
            return render(request, 'rentals/return_confirmation.html')
    else:
        rental = Rental.objects.get(id=rental)
        url = reverse('rentals:return_equipment', args=(rental.id,))
        form = ReturnEquipmentForm(user=rental.user,
                                   rental=rental,
                                   data={
                                       'equipment': rental.rentalitem_set.filter(returned=False),
                                       'deposit': rental.deposit,
                                       'belt_weight': rental.weight,
                                   })

    context = {
        'form': form,
        'url': url,
        'rental_user': form.user,
        'title': _('Return Equipment'),
        'show_cost': False,
    }
    return render(request, 'rentals/rent_equipment.html', context)

def user_is_staff_check(user):
    return user.is_staff

@user_passes_test(user_is_staff_check)
def view_admin_log(request):
    admin_log = LogEntry.objects.order_by('-action_time')[:50]
    return render(request, 'rentals/admin_log.html', {'admin_log': admin_log})
