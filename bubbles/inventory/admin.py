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
