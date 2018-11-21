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
from django.conf import settings
from django.db import models
from bubbles.inventory.models import *
from django.utils.translation import gettext_lazy as _

class RentalPeriod(models.Model):
    start_date = models.DateField(_('Start date'))
    end_date = models.DateField(_('End date'), null=True)
    default_deposit = models.IntegerField(_('Deposit'))
    default_cost_per_item = models.IntegerField(_('Cost per item'))
    hidden = models.BooleanField(default=False)

    def __str__(self):
        if self.end_date:
            return "{} - {}".format(self.start_date,
                                    self.end_date)
        return "{} -".format(self.start_date)

class Rental(models.Model):
    REQUESTED = 'REQ'
    RENTED = 'REN'
    RETURNED = 'RET'
    STATE_CHOICES = (
        (REQUESTED, _('Requested')),
        (RENTED, _('Rented')),
        (RETURNED, _('Returned')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL,
                                    limit_choices_to={'is_staff': True},
                                    related_name='approved_rentals_set',
                                    null=True, blank=True)
    state = models.CharField(_('State'),
                             max_length=3,
                             choices=STATE_CHOICES,
                             default=REQUESTED)
    deposit = models.IntegerField(_('Deposit'))
    notes = models.TextField(_('Notes'), null=True, blank=True)
    deposit_returned = models.BooleanField(_('Deposit returned'), default=True)
    rental_period = models.ForeignKey(RentalPeriod, on_delete=models.CASCADE)

    def __str__(self):
        return "Rental by {} for {}".format(self.user, self.rental_period)

class RentalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cost = models.IntegerField(_('Cost'), default=0)
    returned = models.BooleanField(_('Returned'), default=False)

    def __str__(self):
        if self.rental:
            return "{} to {}".format(self.item, self.rental.user)
        return "{} to unknown".format(self.item)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.rental == other.rental and self.item == other.item and self.cost == other.cost
        return NotImplemented

class RequestItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, null=True)
    item_description = models.CharField(_('Type'), max_length=255)
    item_size = models.CharField(_('Size'), max_length=2, null=True, blank=True)
    cost = models.IntegerField(_('Cost'), default=0)

    def __str__(self):
        if self.rental:
            return "{} to {}".format(self.item_description, self.rental.user)
        return "{} to unknown".format(self.item_description)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.rental == other.rental and self.item_description == other.item_description and self.item_size == other.item_size
        return NotImplemented
