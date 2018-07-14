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
from datetime import timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

class Item(models.Model):
    """
    Represents an item of equipment
    """
    AVAILABLE = 'A'
    IN_USE = 'U'
    BROKEN = 'B'
    REPAIR = 'R'
    CONDEMNED = 'C'
    STATE_CHOICES = (
        (AVAILABLE, _('Available')),
        (IN_USE, _('In use')),
        (BROKEN, _('Broken')),
        (REPAIR, _('Repair')),
        (CONDEMNED, _('Condemned')),
    )

    def get_next_number():
        """
        Calculates the next number for an item

        :returns: a number if one can be calculated or None if there are no
                  numbers for the item type.
        """
        # TODO: Filter by description
        results = Item.objects.all().order_by('-number')
        for result in results:
            try:
                current_number = int(result.number)
                return current_number + 1
            except:
                pass
        return None

    number = models.CharField(_('Number'), max_length=5, default=get_next_number)
    manufacturer = models.CharField(_('Manufacturer'), max_length=255)
    date_of_purchase = models.DateField(_('Date of purchase'))
    state = models.CharField(_('State'), max_length=1, choices=STATE_CHOICES, default=STATE_CHOICES[0])
    description = models.CharField(_('Type'), max_length=255)

    def __str__(self):
        return '{} {} ({})'.format(self.manufacturer, self.description, self.number)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.number == other.number and self.description == other.description
        return NotImplemented

class BCD(Item):
    SMALL = 'S'
    MEDIUM = 'M'
    MEDIUM_LARGE = 'ML'
    LARGE = 'L'
    SIZE_CHOICES = (
        (SMALL, _('Small')),
        (MEDIUM, _('Medium')),
        (MEDIUM_LARGE, _('Medium large')),
        (LARGE, _('Large')),
    )

    last_service = models.DateField(_('Last service'))
    size = models.CharField(_('Size'), max_length=2, choices=SIZE_CHOICES)

    @property
    def next_service(self):
        return self.last_service + timedelta(weeks=52)

    def clean(self):
        self.description = "BCD"

    class Meta:
        verbose_name = 'BCD'

class Booties(Item):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'
    SIZE_CHOICES = (
        (SMALL, _('Small')),
        (MEDIUM, _('Medium')),
        (LARGE, _('Large')),
        (EXTRA_LARGE, _('Extra large')),
    )

    size = models.CharField(_('Size'), max_length=2, choices=SIZE_CHOICES)

    def clean(self):
        self.description = "Booties"

    class Meta:
        verbose_name_plural = 'Booties'

class Cylinder(Item):
    serial_num = models.CharField(_('Serial number'), max_length=255, primary_key=True)
    material = models.CharField(_('Material'), max_length=255)
    capacity = models.DecimalField(_('Capacity'), max_digits=4, decimal_places=2)
    last_viz = models.DateField(_('Last visual inspection'))
    last_hydro = models.DateField(_('Last hydro-static inspection'))
    viz_period = models.DurationField(_('Visual inspection validity period'), default=timedelta(weeks=52))
    hydro_period = models.DurationField(_('Hydro-static test validity period'), default=timedelta(weeks=104))

    @property
    def next_service(self):
        return min(self.last_viz + self.viz_period, self.last_hydro + self.hydro_period)

    @property
    def last_service(self):
        return max(self.last_viz, self.last_hydro)

    def clean(self):
        self.description = "Cylinder"

class Fins(Item):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'
    SIZE_CHOICES = (
        (SMALL, _('Small')),
        (MEDIUM, _('Medium')),
        (LARGE, _('Large')),
        (EXTRA_LARGE, _('Extra large')),
    )

    size = models.CharField(_('Size'), max_length=2, choices=SIZE_CHOICES)

    def clean(self):
        self.description = "Fins"

    class Meta:
        verbose_name_plural = 'Fins'

class Regulator(Item):
    last_service = models.DateField(_('Last service'))

    @property
    def next_service(self):
        return self.last_service + timedelta(weeks=52)

    def clean(self):
        self.description = "Regulator"

class Weight(models.Model):
    total_weight = models.IntegerField(_('Total weight'))
    available_weight = models.IntegerField(_('Available weight'))

class WeightBelt(models.Model):
    IN_USE = 'U'
    BROKEN = 'B'
    CONDEMNED = 'C'
    STATE_CHOICES = (
        (IN_USE, _('In use')),
        (BROKEN, _('Broken')),
        (CONDEMNED, _('Condemned')),
    )

    date_of_purchase = models.DateField(_('Date of purchase'))
    state = models.CharField(_('State'), max_length=1, choices=STATE_CHOICES)

class Wetsuit(Item):
    SMALL = 'S'
    MEDIUM = 'M'
    MEDIUM_LARGE = 'ML'
    LARGE = 'L'
    EXTRA_LARGE = 'XL'
    SIZE_CHOICES = (
        (SMALL, _('Small')),
        (MEDIUM, _('Medium')),
        (MEDIUM_LARGE, _('Medium large')),
        (LARGE, _('Large')),
        (EXTRA_LARGE, _('Extra large')),
    )

    size = models.CharField(_('Size'), max_length=2, choices=SIZE_CHOICES)

    def clean(self):
        self.description = "Wetsuit"
