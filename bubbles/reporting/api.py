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
from django.db.models import Q
from django.http import JsonResponse

from bubbles.inventory import get_size_breakdown
from bubbles.inventory.models import Item

def equipment_size(request, item_type):
    state_filter = ~Q(state=Item.CONDEMNED)
    size_count = get_size_breakdown(item_type, state_filter)
    result = []
    for k,v in size_count.items():
        result.append({'name': k, 'value': v})
    return JsonResponse({'sizeCount': result})

