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

from django.test import TestCase
from bubbles.inventory import get_item_size_map, get_sizes
from bubbles.inventory.models import BCD, Item

class StaticFunctionTest(TestCase):
    def test_get_sizes_available(self):
        date_of_purchase = datetime.date(year=2018, month=7, day=2)
        item = BCD(number='1',
                   manufacturer='test',
                   date_of_purchase=date_of_purchase,
                   state = BCD.AVAILABLE,
                   size = BCD.LARGE,
                   last_service=date_of_purchase,
                   description='BCD')
        item.save()
        results = get_sizes(BCD)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], BCD.LARGE)

    def test_get_sizes_none(self):
        results = get_sizes(BCD)
        self.assertEqual(len(results), 0)

    def test_get_item_size_map(self):
        date_of_purchase = datetime.date(year=2018, month=7, day=2)
        item = BCD(number='1',
                   manufacturer='test',
                   date_of_purchase=date_of_purchase,
                   state = BCD.AVAILABLE,
                   size = BCD.LARGE,
                   last_service=date_of_purchase,
                   description='BCD')
        item.save()
        item_size_map = get_item_size_map()
        self.assertEqual(len(item_size_map['BCD']), 1)
        self.assertEqual(len(item_size_map['Booties']), 0)
