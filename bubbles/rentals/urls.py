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
"""bubbles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = "rentals"

urlpatterns = [
    path("", views.index, name="index"),
    path("request/", views.request_equipment, name="request_equipment"),
    path(
        "request/<int:request_id>/", views.request_equipment, name="request_equipment"
    ),
    path("rent/", views.rent_equipment, name="rent_equipment"),
    path("rent/<int:rental_request>/", views.rent_equipment, name="rent_equipment"),
    path(
        "rent/<int:rental_request>/save/",
        views.save_rental_request,
        name="save_rental_request",
    ),
    path("return/<int:rental_id>/", views.return_equipment, name="return_equipment"),
    path("admin/admin_log/", views.view_admin_log, name="view_admin_log"),
]
