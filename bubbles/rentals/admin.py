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
import locale

from django.db.models import DateField, DurationField, IntegerField
from django.contrib import admin
from django.forms import DateInput, NumberInput, TextInput
from django.utils.translation import gettext_lazy as _

from bubbles.admin import admin_site, BUBBLES_FORMFIELD_OVERRIDES

from . import models


@admin.register(models.Rental, site=admin_site)
class RentalAdmin(admin.ModelAdmin):
    @admin.display(ordering="rental_period__start_date")
    def start_date(self, obj):
        return obj.rental_period.start_date

    @admin.display(ordering="rental_period__end_date")
    def end_date(self, obj):
        return obj.rental_period.end_date

    @admin.display(
        description=_("user"),
        ordering="user",
    )
    def formatted_username(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return (
                obj.user.first_name
                + " "
                + obj.user.last_name
                + " ("
                + str(obj.user)
                + ")"
            )
        else:
            return obj.user

    list_display = ("formatted_username", "start_date", "end_date", "state")
    date_hierarchy = "rental_period__start_date"
    list_filter = ("state",)
    ordering = ["-rental_period__start_date"]
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES


@admin.register(models.RentalPeriod, site=admin_site)
class RentalPeriodAdmin(admin.ModelAdmin):
    def deposit(self, obj):
        return f"R{obj.default_deposit}"

    def cost_per_item(self, obj):
        return f"R{obj.default_cost_per_item}"

    list_display = ("name", "start_date", "end_date", "deposit", "cost_per_item")
    exclude = ["hidden"]
    date_hierarchy = "start_date"
    ordering = ["-start_date"]
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES


@admin.register(models.RentalItem, site=admin_site)
class RentalItemAdmin(admin.ModelAdmin):
    @admin.display(ordering="item__number")
    def number(self, obj):
        return obj.item.number

    @admin.display(
        description=_("item"),
        ordering="item__description",
    )
    def description(self, obj):
        return obj.item.description

    @admin.display(ordering="rental__user")
    def user(self, obj):
        if obj.rental:
            return obj.rental.user
        else:
            return None

    list_display = ("description", "number", "user", "returned")
    list_filter = ("returned",)
    ordering = ["rental__user"]
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES


@admin.register(models.RequestItem, site=admin_site)
class RequestItemAdmin(admin.ModelAdmin):
    @admin.display(ordering="item__size")
    def size(self, obj):
        return obj.item_size

    @admin.display(
        description=_("item"),
        ordering="item_description",
    )
    def description(self, obj):
        return obj.item_description

    @admin.display(ordering="rental__user")
    def user(self, obj):
        if obj.rental:
            return obj.rental.user
        else:
            return None

    list_display = ("description", "size", "user")
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES
