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
import sys

from django import forms
from django.forms import fields, widgets
from django.utils.translation import gettext_lazy as _

from bubbles.inventory.models import BCD, Booties, Cylinder, Fins, Wetsuit, Item
from .models import RentalItem

def get_sizes(item_type, size_tag='size'):
    sizes_set = item_type.objects.filter(state__exact=Item.AVAILABLE).values(size_tag).distinct()
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

class EquipmentTableWidget(widgets.MultiWidget):
    template_name = 'rentals/widgets/equipment_table_widget.html'

    def __init__(self, widgets=[], **kwargs):
        super().__init__(widgets, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        item_types = Item.objects.filter(state__exact=Item.AVAILABLE).values('description').distinct()
        context['widget']['item_size_map'] = get_item_size_map()
        context['widget']['item_types'] = item_types
        context['widget']['show_number'] = self.show_number
        return context

    def value_from_datadict(self, data, files, names):
        self.widgets = []
        try:
            # Python created with data
            rental = data['equipment']
            self.add_items(rental.rentalitem_set.all())
        except KeyError:
            # Response with POST data
            for key in data:
                if 'csrf' in key:
                    continue
                value = data.getlist(key)
                for i in range(0, len(value), 4):
                    description = value[i]
                    number = value[i + 1]
                    size = value[i + 2]
                    if size == "N/A":
                        size = None
                    cost = value[i + 3]
                    self.add_item(description, number, size, cost)
        return super().value_from_datadict(data, files, names)

    def decompress(self, value):
        return value

    def add_item(self, item_description, item_number, item_size, item_cost=0):
        widget = EquipmentRowWidget(item_description,
                                    item_number=item_number,
                                    item_size=item_size,
                                    item_cost=item_cost,
                                    show_number=self.show_number)
        self.widgets.append(widget)


    def add_items(self, items):
        for rental_item in items:
            # Get subclass object
            item = getattr(rental_item.item, rental_item.item.description.lower())
            try :
                self.add_item(item.description, item.number, item.size, rental_item.cost)
            except AttributeError:
                self.add_item(item.description, item.number, None, rental_item.cost)

    class Media:
        css = {
            'screen': ('css/equipment_table.css',),
        }
        js = ('js/equipment_table.js',)

class EquipmentRowWidget(widgets.Widget):
    template_name = 'rentals/widgets/equipment_item_widget.html'
    show_number = False

    def __init__(self, item_description, item_size=None, item_number='',
                 item_cost=0, show_number=False, **kwargs):
        super().__init__(**kwargs)
        self.item_description = item_description
        self.item_size = item_size
        self.item_number = item_number
        self.item_cost = item_cost
        self.show_number = show_number

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        try:
            sizes = get_item_size_map()[self.item_description]
        except KeyError:
            sizes = None
        context['widget']['show_number'] = self.show_number
        context['widget']['item_description'] = self.item_description
        context['widget']['item_size'] = self.item_size
        context['widget']['item_sizes'] = sizes
        context['widget']['item_number'] = self.item_number
        context['widget']['item_cost'] = self.item_cost
        return context

class EquipmentListField(fields.Field):
    widget = EquipmentTableWidget

    def __init__(self, show_number=False, **kwargs):
        super().__init__(**kwargs)
        self.widget.show_number = show_number

    def clean(self, value):
        if value in self.empty_values:
            return None
        rental_items = []
        errors = []
        for i, widget in enumerate(self.widget.widgets):
            # TODO: Currently assumes RentalItem exist.
            try:
                item = Item.objects.get(number=widget.item_number,
                                        description=widget.item_description,
                                        state=Item.AVAILABLE)
            except:
                errors.append(forms.ValidationError(_('%(type)s number %(num)s not found'),
                                            code='invalid',
                                            params={
                                                'type': widget.item_description,
                                                'num': widget.item_number,
                                            }))
                continue
            rental_item = RentalItem.objects.get(item=item)
            rental_items.append(rental_item)
        if len(errors) > 0:
            raise forms.ValidationError(errors)
        return rental_items

class RequestEquipmentForm(forms.Form):
    equipment = EquipmentListField()

class RentEquipmentForm(forms.Form):
    equipment = EquipmentListField(show_number=True)
