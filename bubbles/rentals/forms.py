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
import decimal
import sys

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.forms import fields, widgets
from django.utils.translation import gettext_lazy as _

from bubbles.inventory.models import BCD, Booties, Cylinder, Fins, Wetsuit, Item, Weight
from .models import Rental, RentalItem, RentalPeriod, RequestItem

def get_sizes(item_type, size_tag='size'):
    sizes_set = item_type.objects.filter(state__exact=Item.AVAILABLE, hidden=False).values(size_tag).distinct()
    sizes = [i[size_tag] for i in sizes_set]
    return sizes

def get_item_size_map():
    item_size_map = {}
    item_size_map['BCD'] = get_sizes(BCD)
    item_size_map['Booties'] = get_sizes(Booties)
    item_size_map['Cylinder'] = get_sizes(Cylinder, 'capacity')
    item_size_map['Fins'] = get_sizes(Fins)
    item_size_map['Wetsuit'] = get_sizes(Wetsuit)
    return item_size_map

def get_initial_period():
    date = datetime.date.today()
    period_query_set = RentalPeriod.objects.filter(end_date__gt=date, hidden=False)
    if len(period_query_set) > 0:
        return period_query_set[0]
    return None

class EquipmentTableWidget(widgets.MultiWidget):
    template_name = 'rentals/widgets/equipment_table_widget.html'

    def __init__(self, show_number=False, show_cost=False, item_cost=0,
                 widgets=[], **kwargs):
        super().__init__(widgets, **kwargs)
        self.item_cost = item_cost
        self.show_number = show_number
        self.show_cost = show_cost

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        item_types = Item.objects.filter(state=Item.AVAILABLE,
                                         hidden=False).values('description').distinct()
        free_items = Item.objects.filter(state=Item.AVAILABLE,
                                         free=True).values('description').distinct()
        context['widget']['item_size_map'] = get_item_size_map()
        context['widget']['item_types'] = item_types
        context['widget']['free_items'] = free_items
        context['widget']['item_cost'] = self.item_cost
        context['widget']['show_number'] = self.show_number
        context['widget']['show_cost'] = self.show_cost
        return context

    def value_from_datadict(self, data, files, names):
        self.widgets = []
        try:
            # Python created with data
            rental_items = data['equipment']
            if len(rental_items) > 0:
                if type(rental_items[0]) == RentalItem:
                    self.add_items(rental_items)
                else:
                    self.add_request_items(rental_items)
        except KeyError:
            # Response with POST data
            item_types = Item.objects.filter(hidden=False).values('description').distinct()
            item_types = [i['description'] for i in item_types]
            for key in data:
                if key not in item_types:
                    continue
                value = data.getlist(key)
                range_step = 2
                if self.show_number:
                    range_step += 1
                if self.show_cost:
                    range_step += 1
                for i in range(0, len(value), range_step):
                    description = value[i]
                    size = value[i + 1]
                    if size == 'N/A':
                        size = None
                    cost = 0
                    if self.show_cost:
                        cost = value[i + 3]
                    number = None
                    if self.show_number:
                        number = value[i + 2]
                    self.add_item(description, number, size, cost)
        return super().value_from_datadict(data, files, names)

    def decompress(self, value):
        return value

    def add_item(self, item_description, item_number, item_size, item_cost=0):
        if item_description == 'Cylinder':
            item_size = decimal.Decimal(item_size)

        widget = EquipmentRowWidget(item_description,
                                    item_number=item_number,
                                    item_size=item_size,
                                    item_cost=item_cost,
                                    show_number=self.show_number,
                                    show_cost=self.show_cost)
        self.widgets.append(widget)

    def add_request_items(self, items):
        for request in items:
            self.add_item(request.item_description,
                          '',
                          request.item_size,
                          request.cost)

    def add_items(self, items):
        for rental_item in items:
            try :
                # Get subclass object
                item = getattr(rental_item.item,
                               rental_item.item.description.lower())
                self.add_item(item.description,
                              item.number,
                              item.size,
                              rental_item.cost)
            except AttributeError:
                # No subclass to be had
                item = rental_item.item
                self.add_item(item.description,
                              item.number,
                              None,
                              rental_item.cost)

    class Media:
        css = {
            'screen': ('css/equipment_table.css',),
        }
        js = ('vendor/gijgo/js/gijgo.min.js', 'js/equipment_table.js',)

class EquipmentRowWidget(widgets.Widget):
    template_name = 'rentals/widgets/equipment_item_widget.html'
    show_number = False

    def __init__(self, item_description, item_size=None, item_number='',
                 item_cost=0, show_number=False, show_cost=False, **kwargs):
        super().__init__(**kwargs)
        self.item_description = item_description
        self.item_size = item_size
        self.item_number = item_number
        self.item_cost = item_cost
        self.show_number = show_number
        self.show_cost = show_cost

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        try:
            sizes = get_item_size_map()[self.item_description] + [ self.item_size ]
        except KeyError:
            sizes = None
        context['widget']['show_number'] = self.show_number
        context['widget']['show_cost'] = self.show_cost
        context['widget']['item_description'] = self.item_description
        context['widget']['item_size'] = self.item_size
        context['widget']['item_sizes'] = sizes
        context['widget']['item_number'] = self.item_number
        context['widget']['item_cost'] = self.item_cost
        return context

class EquipmentListField(fields.Field):
    widget = EquipmentTableWidget

    def __init__(self, show_number=False, show_cost=False,
                 item_cost=0, **kwargs):
        super().__init__(**kwargs)
        self.widget.show_number = show_number
        self.widget.show_cost = show_cost
        self.widget.item_cost = item_cost

    def clean(self, value):
        if value in self.empty_values:
            return None
        rental_items = []
        errors = []
        for i, widget in enumerate(self.widget.widgets):
            try:
                item = Item.objects.get(number=widget.item_number,
                                        description=widget.item_description,
                                        hidden=False)
            except ObjectDoesNotExist:
                if widget.item_number == None or widget.item_number == '':
                    # Rental request
                    request_item = RequestItem(item_description=widget.item_description,
                                               item_size=widget.item_size)
                    if request_item not in rental_items:
                        rental_items.append(request_item)
                else:
                    errors.append(forms.ValidationError(
                        _('%(type)s number %(num)s not found'),
                        code='invalid',
                        params={
                            'type': widget.item_description,
                            'num': widget.item_number,
                        }))
                continue
            except Item.MultipleObjectsReturned:
                    errors.append(forms.ValidationError(
                        _('There are multiple %(type)s with number %(num)s. Please renumber one before continuing.'),
                        code='invalid',
                        params={
                            'type': widget.item_description,
                            'num': widget.item_number,
                        }))
                    continue
            try:
                rental_item = RentalItem.objects.get(item=item, returned=False)
            except ObjectDoesNotExist:
                rental_item = RentalItem(item=item,cost=int(widget.item_cost))
            rental_items.append(rental_item)
        if len(errors) > 0:
            raise forms.ValidationError(errors)
        return rental_items

class EquipmentForm(forms.Form):
    period_state_filter = Rental.REQUESTED
    belt_weight = forms.IntegerField(min_value=0,
                                max_value=15,
                                initial=0,
                                widget=widgets.NumberInput(attrs={
                                    'class': 'form-control'}))

    def __init__(self, user, rental=None, request_id=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.rental = rental
        self.request_id = request_id
        if user.is_staff:
            # Staff should not select a period
            period_query_set = RentalPeriod.objects.filter(start_date=None)
        else:
            date = datetime.date.today()
            period_query_set = RentalPeriod.objects.filter(end_date__gt=date,
                                                           hidden=False)
        self.fields['period'] = forms.ModelChoiceField(queryset=period_query_set,
                                    required=False,
                                    widget=widgets.Select(
                                        attrs={'class': 'form-control'}),
                                    initial=get_initial_period)
        # Move period to beginning of the form
        self.fields.move_to_end('period', last=False)

    def clean_period(self):
        if self.cleaned_data['period'] == None:
            if not self.user.is_staff:
                raise forms.ValidationError(_('This field is required'), code='invalid')
            else:
                current_rentals = Rental.objects.filter(user=self.user,
                                                        state=Rental.RENTED)
                if current_rentals.count() > 0:
                    return current_rentals.first().rental_period
                else:
                    return RentalPeriod(start_date=datetime.date.today(),
                                        default_deposit=0,
                                        default_cost_per_item=0,
                                        hidden=True)
        current_period = self.cleaned_data['period']
        existing_periods = Rental.objects.filter(user=self.user,
                                                 rental_period=current_period,
                                                 state=self.period_state_filter)
        if existing_periods.count() and self.request_id == None:
            raise forms.ValidationError(_('You already have a request submitted for '
            'this period'), code='invalid')
        return self.cleaned_data['period']

    def clean_belt_weight(self):
        if self.cleaned_data['belt_weight'] == None:
            raise forms.ValidationError(_('This field is required'), code='invalid')
        total_weight = Weight.objects.first()
        if total_weight == None:
            raise forms.ValidationError(_('No total weight specified by staff, unable to continue.' +
            'Please send this error to your system administrator.'), code='invalid')
        return self.cleaned_data['belt_weight']


    def clean(self):
        if not self.has_error('period'):
            if self.rental == None:
                state = Rental.REQUESTED
                period = self.cleaned_data['period']
                deposit = period.default_deposit
                self.rental = Rental(user=self.user,
                                     state=state,
                                     deposit=deposit,
                                     rental_period=period)
            try:
                free_items = Item.objects.filter(state__exact=Item.AVAILABLE,
                                                 free=True).values('description').distinct()
                free_items = [x['description'] for x in free_items]
                for rental_item in self.cleaned_data['equipment']:
                    rental_item.rental = self.rental
                    try:
                        if rental_item.item_description not in free_items:
                            rental_item.cost = self.rental.rental_period.default_cost_per_item
                    except AttributeError:
                        pass # Only Request Items have item_description
            except (KeyError, TypeError):
                pass
        return self.cleaned_data

class RequestEquipmentForm(EquipmentForm):
    equipment = EquipmentListField()
    liability = forms.BooleanField(
        label=mark_safe(_("I have read and understand the <a href=/docs/terms>terms of rental</a>")),
        widget=widgets.CheckboxInput(attrs={'class': 'form-check-input'}))
    period_state_filter = Rental.REQUESTED

class RentEquipmentForm(EquipmentForm):
    equipment = EquipmentListField(show_number=True, show_cost=True)
    deposit = forms.IntegerField(
        widget=widgets.NumberInput(attrs={'class': 'form-control'}))
    period_state_filter = Rental.RENTED

    def __init__(self, user, rental=None, **kwargs):
        super().__init__(user, rental, **kwargs)
        if rental:
            self.fields['equipment'].widget.item_cost = rental.rental_period.default_cost_per_item

    def clean(self):
        super().clean()
        rented_equipment = self.cleaned_data.get('equipment')
        if rented_equipment:
            for item in rented_equipment:
                try:
                    item = item.item
                    if item.state != Item.AVAILABLE:
                        self.add_error('equipment', forms.ValidationError(
                            _('%(type)s number %(num)s not available'),
                            code='invalid',
                            params={
                                'type': item.description,
                                'num': item.number,
                            }))
                except AttributeError:
                    self.add_error('equipment', forms.ValidationError(
                        _('%(type)s number not valid'),
                        code='invalid',
                        params={
                            'type': item.item_description,
                        }))

class ReturnEquipmentForm(forms.Form):
    belt_weight = forms.IntegerField(min_value=0,
                                max_value=15,
                                initial=0,
                                widget=widgets.NumberInput(attrs={'class': 'form-control'}))
    equipment = EquipmentListField(show_number=True)
    deposit = forms.IntegerField(
        widget=widgets.NumberInput(attrs={'class': 'form-control',
                                          'readonly': True}))
    deposit_returned = forms.BooleanField(required=False,
        widget=widgets.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, user, rental, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.rental = rental
