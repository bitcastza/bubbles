###########################################################################
# Bubbles is Copyright (C) 2018-2019 Kyle Robbertze <krobbertze@gmail.com>
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
from django import forms
from django.db.models import Q
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from .models import Item

class InventoryCheckForm(forms.Form):
    def __init__(self, item_type, state, **kwargs):
        super().__init__(**kwargs)
        if item_type == Item:
            q_filter = ~Q(description__exact='BCD') & \
                    ~Q(description__exact='Booties') & \
                    ~Q(description__exact='Cylinder') & \
                    ~Q(description__exact='Fins') & \
                    ~Q(description__exact='Regulator') & \
                    ~Q(description__exact='Wetsuit')
            q_filter = q_filter & Q(state=state)
            show_description = True
        else:
            q_filter = Q(state=state)
            show_description = False

        items = item_type.objects.filter(q_filter).order_by('description', 'number')
        self.item_state = Item.STATE_MAP[state]
        for item in items:
            label = ""
            if show_description:
                label += item.description + ': '
            label += item.number + ' (' + item.manufacturer + ')'
            self.fields[item.id] = forms.BooleanField(
                label=_(label),
                required=False,
                widget=widgets.CheckboxInput(attrs={
                    'class': 'form-check-input'
                }))

class BaseInventoryCheckFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['state'] = Item.STATE_CHOICES[index][0]
        return kwargs
