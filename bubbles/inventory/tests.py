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
    @classmethod
    def setUpTestData(cls):
        last_viz = datetime.date(year=2018, month=7, day=2)
        cls.next_service = datetime.date(year=2019, month=7, day=1)
        cls.cylinder = Cylinder.objects.create(number='1',
                                 manufacturer='test',
                                 date_of_purchase=last_viz,
                                 state=Item.AVAILABLE,
                                 description='Cylinder',
                                 serial_num='123',
                                 material='steel',
                                 capacity=12,
                                 last_viz=last_viz,
                                 last_hydro=last_viz)

    def setUp(self):
        self.cylinder.refresh_from_db()

    def test_next_service_viz(self):
        self.assertEqual(self.cylinder.next_service, self.next_service)

    def test_next_service_hydro(self):
        last_service = datetime.date(year=2018, month=8, day=1)
        self.cylinder.last_hydro = last_service
        self.cylinder.hydro_period = datetime.timedelta(weeks=1)

        self.assertEqual(self.cylinder.next_service,
                         last_service + self.cylinder.hydro_period)

    def test_last_service_hydro(self):
        last_service = datetime.date(year=2018, month=8, day=1)
        self.cylinder.last_hydro = last_service
        self.assertEqual(self.cylinder.last_service, last_service)

    def test_last_service_viz(self):
        last_service = datetime.date(year=2018, month=8, day=1)
        self.cylinder.last_viz = last_service
        self.assertEqual(self.cylinder.last_service, last_service)

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
