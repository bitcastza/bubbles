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
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import RentalItem, Rental
from bubbles.inventory.models import Item, Weight


@receiver(pre_delete, sender=RentalItem)
def handle_delete_rental_item(sender, instance, using, **kwargs):
    instance.item.state = Item.AVAILABLE
    instance.item.save()


@receiver(pre_delete, sender=Rental)
def handle_delete_rental(sender, instance, using, **kwargs):
    total_weight = Weight.objects.first()
    total_weight.available_weight = total_weight.available_weight + instance.weight
    total_weight.save()


@receiver(post_save, sender=RentalItem)
def handle_edit_rentalitem(sender, instance, created, raw, using, **kwargs):
    if not raw:
        rental = instance.rental
        if rental != None:
            # Update rental if all rental items are returned
            if not rental.rentalitem_set.filter(returned=False).exists():
                rental.state = Rental.RETURNED
                rental.save()
            else:
                rental.state = Rental.RENTED
                rental.save()

        # Update item if rental item changes
        if instance.returned:
            instance.item.state = Item.AVAILABLE
        else:
            instance.item.state = Item.IN_USE
        instance.item.save()
