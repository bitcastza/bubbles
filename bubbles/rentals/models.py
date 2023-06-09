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
import datetime

from django.conf import settings
from django.db import models
from bubbles.inventory.models import Item
from django.utils.translation import gettext_lazy as _


class RentalPeriod(models.Model):
    start_date = models.DateField(_("Start date"))
    end_date = models.DateField(_("End date"), null=True)
    default_deposit = models.IntegerField(_("Deposit"))
    default_cost_per_item = models.IntegerField(_("Cost per item"))
    name = models.CharField(_("Name"), max_length=255)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        if self.end_date:
            return f"{self.name} ({self.start_date} - {self.end_date})"
        return f"{self.name} ({self.start_date} -)"


class Rental(models.Model):
    REQUESTED = "REQ"
    RENTED = "REN"
    RETURNED = "RET"
    STATE_CHOICES = (
        (REQUESTED, _("Requested")),
        (RENTED, _("Rented")),
        (RETURNED, _("Returned")),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_staff": True},
        related_name="approved_rentals_set",
        null=True,
        blank=True,
    )
    state = models.CharField(
        _("State"), max_length=3, choices=STATE_CHOICES, default=REQUESTED
    )
    deposit = models.IntegerField(_("Deposit"))
    notes = models.TextField(_("Notes"), null=True, blank=True)
    deposit_returned = models.BooleanField(_("Deposit returned"), default=True)
    rental_period = models.ForeignKey(RentalPeriod, on_delete=models.CASCADE)
    weight = models.IntegerField(_("Weight"), null=True, blank=True)

    class Meta:
        permissions = [
            ("free_rental", "Can rent gear without paying"),
        ]

    def is_overdue(self):
        today = datetime.date.today()
        if self.rental_period.end_date:
            return self.rental_period.end_date < today
        else:
            return False

    def is_due(self):
        today = datetime.date.today()
        if self.rental_period.end_date:
            return self.rental_period.end_date == today
        else:
            return False

    def __str__(self):
        return f"Rental by {self.user} for {self.rental_period}"


class RentalItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cost = models.IntegerField(_("Cost"), default=0)
    returned = models.BooleanField(_("Returned"), default=False)

    def __str__(self):
        if self.rental:
            return f"{self.item} to {self.rental.user}"
        return f"{self.item} to unknown"

    def __eq__(self, other):
        try:
            return self.pk == other.pk and self.returned == other.returned
        except AttributeError:
            return False

    def __hash__(self):
        return self.pk ^ self.returned


class RequestItem(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, null=True)
    item_description = models.CharField(_("Type"), max_length=255)
    item_size = models.CharField(_("Size"), max_length=3, null=True, blank=True)
    cost = models.IntegerField(_("Cost"), default=0)
    item_number = models.CharField(_("Number"), max_length=5, null=True, blank=True)

    def __str__(self):
        if self.rental:
            return f"{self.item_description} to {self.rental.user}"
        return f"{self.item_description} to unknown"
