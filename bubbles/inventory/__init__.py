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
from django.db.models import Count, Q

def get_sizes(item_type, state_filter=None):
    from bubbles.inventory.models import Item
    size_tag = 'size'
    if state_filter is None:
        state_filter = Q(state=Item.AVAILABLE) & Q(hidden=False)

    sizes_set = item_type.objects.filter(state_filter).values(size_tag).distinct()
    sizes = [i[size_tag] for i in sizes_set]
    return sizes

def get_item_size_map(state_filter=None):
    from bubbles.inventory.models import BCD, Booties, Cylinder, Fins, Wetsuit
    item_size_map = {}
    item_size_map['BCD'] = get_sizes(BCD, state_filter)
    item_size_map['Booties'] = get_sizes(Booties, state_filter)
    item_size_map['Cylinder'] = get_sizes(Cylinder, state_filter)
    item_size_map['Fins'] = get_sizes(Fins, state_filter)
    item_size_map['Wetsuit'] = get_sizes(Wetsuit, state_filter)
    return item_size_map

def get_size_breakdown(item_type, state_filter=None):
    sizes = get_item_size_map(state_filter)[item_type]
    size_count = {}
    from bubbles.inventory import models
    for s in sizes:
        flt = Q(size=s)
        if state_filter:
            flt = flt & state_filter
        size_count[s] = getattr(models, item_type).objects.filter(flt).count()
    return size_count

def get_items_in_state(state):
    from bubbles.inventory.models import Item
    items = Item.objects.filter(state=state).values('description').annotate(count=Count('description'))
    result = {}
    for i in items:
        result[i['description']] = i['count']
    return result
