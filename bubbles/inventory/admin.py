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
from bubbles.admin import admin_site

from . import models

admin_site.register(models.Item)
admin_site.register(models.BCD)
admin_site.register(models.Booties)
admin_site.register(models.Cylinder)
admin_site.register(models.Fins)
admin_site.register(models.Regulator)
admin_site.register(models.Weight)
admin_site.register(models.WeightBelt)
admin_site.register(models.Wetsuit)
