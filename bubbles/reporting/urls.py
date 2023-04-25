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
from django.urls import path
from . import views, api

app_name = "reporting"
urlpatterns = [
    path("", views.index, name="index"),
    path("equipment/size", views.equipment_size, name="size"),
    path("equipment/repair", views.equipment_under_repair, name="repair"),
    path("api/equipment/size/<str:item_type>", api.equipment_size, name="api-size"),
]
