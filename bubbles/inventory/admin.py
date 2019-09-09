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
from django.db.models import Q

from bubbles.admin import admin_site, BUBBLES_FORMFIELD_OVERRIDES

from . import models

def make_repair(modeladmin, request, queryset):
    for obj in queryset:
        obj.state = models.Item.REPAIR
        obj.save()

make_repair.short_description = 'Mark selected items as in for repairs'

def make_available(modeladmin, request, queryset):
    for obj in queryset:
        obj.state = models.Item.AVAILABLE
        obj.save()

make_available.short_description = 'Mark available'

def make_missing(modeladmin, request, queryset):
    for obj in queryset:
        obj.state = models.Item.MISSING
        obj.save()

make_missing.short_description = 'Mark missing'

def return_from_repair(modeladmin, request, queryset):
    make_available(modeladmin, request, queryset)
    for obj in queryset:
        today = datetime.date.today()
        date = datetime.date(year=today.year, month=today.month, day=1)
        obj.last_service = date
        obj.save()

return_from_repair.short_description = 'Return items from repair'

@admin.register(models.Item, site=admin_site)
class ItemAdmin(admin.ModelAdmin):
    actions = [make_available, make_repair, return_from_repair, make_missing]
    list_display = ('description', 'number', 'manufacturer', 'state')
    list_filter = ('state', 'description')
    list_display_links = ('number',)
    ordering = ['number']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES
    fieldsets = (
        (None, {
            'fields': ('number',
                       'manufacturer',
                       'date_of_purchase',
                       'state',
                       'description'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('hidden', 'free',),
        })
    )

    def get_queryset(self, request):
        q_filter = ~Q(description__exact='BCD') & \
                ~Q(description__exact='Booties') & \
                ~Q(description__exact='Cylinder') & \
                ~Q(description__exact='Fins') & \
                ~Q(description__exact='Regulator') & \
                ~Q(description__exact='Wetsuit')
        qs = super().get_queryset(request)
        return qs.filter(q_filter)

class SizeAdmin(admin.ModelAdmin):
    actions = [make_available, make_repair, return_from_repair, make_missing]
    list_display = ('number', 'manufacturer', 'size', 'state')
    list_filter = ('state', 'size', 'manufacturer')
    exclude = ['description']
    ordering = ['number']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES
    fieldsets = (
        (None, {
            'fields': ('number',
                       'manufacturer',
                       'date_of_purchase',
                       'state',
                       'size'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('hidden',),
        })
    )

@admin.register(models.BCD, site=admin_site)
class BCDAdmin(SizeAdmin):
    list_display = ('number', 'manufacturer', 'size', 'serial_num', 'next_service', 'state')
    exclude = ['description']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES
    fieldsets = (
        (None, {
            'fields': ('number',
                       'manufacturer',
                       'date_of_purchase',
                       'state',
                       'size',
                       'serial_num',
                       'last_service'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('hidden',),
        })
    )

@admin.register(models.Cylinder, site=admin_site)
class CylinderAdmin(admin.ModelAdmin):
    actions = [make_available, make_repair, return_from_repair, make_missing]
    list_display = ('number',
                    'manufacturer',
                    'serial_num',
                    'size',
                    'last_viz',
                    'state',)
    list_filter = ('state', 'manufacturer', 'size')
    exclude = ['description']
    ordering = ['number']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES
    fieldsets = (
        (None, {
            'fields': ('number',
                       'manufacturer',
                       'date_of_purchase',
                       'state',
                       'serial_num',
                       'material',
                       'size',
                       'last_viz',
                       'last_hydro'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('viz_period', 'hydro_period', 'hidden'),
        })
    )

@admin.register(models.Regulator, site=admin_site)
class RegulatorAdmin(admin.ModelAdmin):
    actions = [make_available, make_repair, return_from_repair, make_missing]
    list_display = ('number',
                    'manufacturer',
                    'serial_num',
                    'next_service',
                    'state')
    list_filter = ('state', 'manufacturer')
    exclude = ['description']
    ordering = ['number']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES
    fieldsets = (
        (None, {
            'fields': ('number',
                       'manufacturer',
                       'date_of_purchase',
                       'state',
                       'serial_num',
                       'last_service'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('hidden',),
        })
    )

@admin.register(models.ItemValue, site=admin_site)
class ItemValueAdmin(admin.ModelAdmin):
    list_display = ('description', 'cost')
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES

admin_site.register(models.Booties, SizeAdmin)
admin_site.register(models.Fins, SizeAdmin)
admin_site.register(models.Weight)
admin_site.register(models.WeightBelt)
admin_site.register(models.Wetsuit, SizeAdmin)
