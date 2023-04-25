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
from django.db.models import DateField, Q
from django.forms.widgets import Select

from .forms import CalendarWidget
from bubbles.inventory.models import BCD, Cylinder, Regulator, Item
from bubbles.rentals.models import Rental

BUBBLES_FORMFIELD_OVERRIDES = {
    DateField: {"widget": CalendarWidget},
}


def get_next_service_set(item_type):
    current_date = datetime.date.today()
    state = Q(state=Item.AVAILABLE) | Q(state=Item.IN_USE)
    items = [
        x for x in item_type.objects.filter(state) if x.next_service < current_date
    ]
    return items


class BubblesAdminSite(admin.AdminSite):
    index_title = None
    index_template = "admin/bubbles/index.html"
    app_index_template = "admin/bubbles/index.html"

    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        extra_context = extra_context or {}
        rental_requests = Rental.objects.filter(state__exact=Rental.REQUESTED)
        rental_returns = Rental.objects.filter(state__exact=Rental.RENTED)
        cylinder_service_set = get_next_service_set(Cylinder)
        regulator_service_set = get_next_service_set(Regulator)
        extra_context["rental_requests"] = rental_requests
        extra_context["rental_returns"] = rental_returns
        extra_context["need_servicing"] = cylinder_service_set + regulator_service_set
        message = request.COOKIES.get("message")
        message_class = request.COOKIES.get("messageclass")
        if message:
            extra_context["messages"] = [
                message,
            ]
            if message_class:
                extra_context["message_class"] = message_class
            else:
                extra_context["message_class"] = "success"
        response = super().index(request, extra_context=extra_context)
        if message:
            response.delete_cookie("message")
        if message_class:
            response.delete_cookie("messageclass")
        return response

    def each_context(self, request):
        context = super().each_context(request)
        context["apps_length"] = len(self.get_app_list(request))
        return context


admin_site = BubblesAdminSite(name="Bubbles Administration")
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
