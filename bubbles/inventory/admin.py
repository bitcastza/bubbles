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
from django.db.models import Q

from bubbles.admin import admin_site, BUBBLES_FORMFIELD_OVERRIDES

from . import models

@admin.register(models.Item, site=admin_site)
class ItemAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        q_filter = ~Q(description__exact='BCD') & \
                ~Q(description__exact='Booties') & \
                ~Q(description__exact='Cylinder') & \
                ~Q(description__exact='Fins') & \
                ~Q(description__exact='Regulator') & \
                ~Q(description__exact='Wetsuit')
        qs = super().get_queryset(request)
        return qs.filter(q_filter)

    list_display = ('description', 'number', 'manufacturer', 'state')
    list_filter = ('state', 'description')
    list_display_links = ('number',)
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES

class SizeAdmin(admin.ModelAdmin):
    list_display = ('number', 'manufacturer', 'size', 'state')
    list_filter = ('state', 'size', 'manufacturer')
    exclude = ['description']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES

@admin.register(models.BCD, site=admin_site)
class BCDAdmin(SizeAdmin):
    list_display = ('number', 'manufacturer', 'size', 'next_service', 'state')
    exclude = ['description']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES

@admin.register(models.Cylinder, site=admin_site)
class CylinderAdmin(admin.ModelAdmin):
    list_display = ('number',
                    'manufacturer',
                    'serial_num',
                    'capacity',
                    'last_viz',
                    'state',)
    list_filter = ('state', 'manufacturer', 'capacity')
    exclude = ['description']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES

@admin.register(models.Regulator, site=admin_site)
class RegulatorAdmin(admin.ModelAdmin):
    list_display = ('number',
                    'manufacturer',
                    'next_service',
                    'state')
    list_filter = ('state', 'manufacturer')
    exclude = ['description']
    formfield_overrides = BUBBLES_FORMFIELD_OVERRIDES

admin_site.register(models.Booties, SizeAdmin)
admin_site.register(models.Fins, SizeAdmin)
admin_site.register(models.Weight)
admin_site.register(models.WeightBelt)
admin_site.register(models.Wetsuit, SizeAdmin)
