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

from bubbles.inventory.models import BCD, Booties, Cylinder, Fins, Wetsuit, Item

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

    def decompress(self, value):
        return value

    def value_from_datadict(self, data, files, names):
        try: # python created with data
            rental = data['equipment']
            self.add_items(rental.rentalitem_set.all())
        except KeyError: # Response with POST data
            for key in data:
                if 'csrf' in key:
                    continue
                value = data.getlist(key)
                for i in range(0, len(value), 2):
                    description = value[i]
                    number = value[i + 1]
                    item_type = getattr(sys.modules['bubbles.rentals.models'], description)
                    item = item_type.objects.get(description=description, number=number)
                    self.add_item(item)
                
        return super().value_from_datadict(data, files, names)

    def add_item(self, item):
        widget = EquipmentRowWidget(item, show_number=self.show_number)
        self.widgets.append(widget)

    def add_items(self, items):
        for item in items:
            self.add_item(item)

    class Media:
        js = ('js/equipment_table.js',)

class EquipmentRowWidget(widgets.Widget):
    template_name = 'rentals/widgets/equipment_item_widget.html'
    show_number = False
    
    def __init__(self, item, show_number=False, **kwargs):
        super().__init__(**kwargs)
        self.item = item
        self.show_number = show_number


    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['show_number'] = self.show_number
        context['widget']['rental_item'] = self.item
        return context

class EquipmentListField(fields.Field):
    widget = EquipmentTableWidget

    def __init__(self, show_number=False, **kwargs):
        super().__init__(**kwargs)
        self.widget.show_number = show_number

    def clean(self, value):
        print(value)
        return super().clean(value)

class RequestEquipmentForm(forms.Form):
    equipment = EquipmentListField()

class RentEquipmentForm(forms.Form):
    equipment = EquipmentListField(show_number=True)
