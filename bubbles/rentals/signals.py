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
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import RentalItem, Rental, Weight
from bubbles.inventory.models import Item

@receiver(pre_delete, sender=RentalItem)
def handle_delete_rental_item(sender, instance, using, **kwargs):
    instance.item.state = Item.AVAILABLE
    instance.item.save()

@receiver(pre_delete, sender=Rental)
def handle_delete_rental(sender, instance, using, **kwargs):
    total_weight = Weight.objects.first()
    total_weight.available_weight = total_weight.available_weight + instance.weight
    total_weight.save()
