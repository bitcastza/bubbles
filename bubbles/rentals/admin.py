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
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from bubbles.admin import admin_site

from . import models

@admin.register(models.Rental, site=admin_site)
class RentalAdmin(admin.ModelAdmin):
    def start_date(self, obj):
        return obj.rental_period.start_date

    def end_date(self, obj):
        return obj.rental_period.end_date

    list_display = ('user', 'start_date', 'end_date', 'state')
    date_hierarchy = 'rental_period__start_date'
    list_filter = ('state',)

@admin.register(models.RentalPeriod, site=admin_site)
class RentalPeriodAdmin(admin.ModelAdmin):
    def deposit(self, obj):
        return "R{}".format(obj.default_deposit)

    def cost_per_item(self, obj):
        return "R{}".format(obj.default_cost_per_item)

    list_display = ('start_date',
                    'end_date',
                    'deposit',
                    'cost_per_item')
    date_hierarchy = 'start_date'

@admin.register(models.RentalItem, site=admin_site)
class RentalItemAdmin(admin.ModelAdmin):
    def number(self, obj):
        return obj.item.number

    def description(self, obj):
        return obj.item.description
    description.short_description = _('item')

    def user(self, obj):
        return obj.rental.user

    list_display = ('description', 'number', 'user')
