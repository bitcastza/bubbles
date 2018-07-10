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

from .models import Item, BCD, Cylinder, Regulator

class BCDTests(TestCase):
    def test_next_service(self):
        last_service = datetime.date(year=2018, month=7, day=2)
        next_service = datetime.date(year=2019, month=7, day=1)
        bcd = BCD.objects.create(number='1',
                                 manufacturer='test',
                                 date_of_purchase=last_service,
                                 state=Item.AVAILABLE,
                                 description='BCD',
                                 last_service=last_service,
                                 size=BCD.SMALL)
        self.assertEqual(bcd.next_service, next_service)

class CylinderTests(TestCase):
    def test_next_service(self):
        last_viz = datetime.date(year=2018, month=7, day=2)
        next_service = datetime.date(year=2019, month=7, day=1)
        cylinder = Cylinder.objects.create(number='1',
                                 manufacturer='test',
                                 date_of_purchase=last_viz,
                                 state=Item.AVAILABLE,
                                 description='BCD',
                                 serial_num='123',
                                 material='steel',
                                 capacity=12,
                                 last_viz=last_viz,
                                 last_hydro=last_viz,
                                 viz_period=datetime.timedelta(weeks=52),
                                 hydro_period=datetime.timedelta(weeks=108))

        self.assertEqual(cylinder.next_service, next_service)

class BCDTests(TestCase):
    def test_next_service(self):
        last_service = datetime.date(year=2018, month=7, day=2)
        next_service = datetime.date(year=2019, month=7, day=1)
        regulator = Regulator.objects.create(number='1',
                                 manufacturer='test',
                                 date_of_purchase=last_service,
                                 state=Item.AVAILABLE,
                                 description='Regulator',
                                 last_service=last_service)
        self.assertEqual(regulator.next_service, next_service)
