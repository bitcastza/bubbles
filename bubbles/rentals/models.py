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
    period = models.DurationField(_('Rental duration'))
    default_deposit = models.IntegerField(_('Deposit'))
    default_cost_per_item = models.IntegerField(_('Cost per item'))

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

    def get_end_date(self):
        return self.start_date + self.period

class RentalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cost = models.IntegerField(_('Cost'), default=0)
