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

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.db.models import DateField, DecimalField, DurationField, CharField,  IntegerField, TextField
from django.forms import NumberInput, TextInput, ModelChoiceField
from django.forms.widgets import Select

from .forms import CalendarWidget
from bubbles.inventory.models import BCD, Cylinder, Regulator
from bubbles.rentals.models import Rental

BUBBLES_FORMFIELD_OVERRIDES = {
    DateField: {'widget': CalendarWidget},
    IntegerField: {
        'widget': NumberInput(attrs={'class': 'vIntegerField form-control'})
    },
    DurationField: {'widget': TextInput(attrs={'class': 'form-control'})},
    TextField: {'widget': TextInput(attrs={'class': 'vTextField form-control'})},
    CharField: {'widget': TextInput(attrs={'class': 'vTextField form-control'})},
    DecimalField: {'widget': NumberInput(attrs={'class': 'form-control'})},
    ModelChoiceField: {'widget': Select(attrs={'class': 'form-control'})},
}

def get_next_service_set(item_type):
    current_date = datetime.date.today()
    items = [x for x in item_type.objects.all() if x.next_service < current_date]
    return items

class BubblesAdminSite(admin.AdminSite):
    index_title = None
    index_template = 'admin/bubbles/index.html'
    app_index_template = 'admin/bubbles/index.html'

    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        extra_context = extra_context or {}
        rental_requests = Rental.objects.filter(state__exact=Rental.REQUESTED)
        rental_returns = Rental.objects.filter(state__exact=Rental.RENTED)
        bcd_service_set = get_next_service_set(BCD)
        cylinder_service_set = get_next_service_set(Cylinder)
        regulator_service_set = get_next_service_set(Regulator)
        extra_context['rental_requests'] = rental_requests
        extra_context['rental_returns'] = rental_returns
        extra_context['need_servicing'] = bcd_service_set + cylinder_service_set + regulator_service_set
        return super(BubblesAdminSite, self).index(request, extra_context=extra_context)

    def each_context(self, request):
        context = super(BubblesAdminSite, self).each_context(request)
        context['apps_length'] = len(self.get_app_list(request))
        return context

admin_site = BubblesAdminSite(name='Bubbles Administration')
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
