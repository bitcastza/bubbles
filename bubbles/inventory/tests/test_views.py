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
from django.contrib.auth.models import User
from django.test import TestCase, Client
from bubbles.inventory.models import Item, BCD, Cylinder, Regulator

class TestInventoryCheck(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = '/inventory/check_inventory'
        cls.client = Client()

    def testItemInventory(self):
        user = User.objects.create_superuser('test',
                                             email='test@example.com',
                                             password='test')
        self.client.login(username='test', password='test')
        last_service = datetime.date(year=2018, month=7, day=2)
        regulator = Regulator.objects.create(number='1',
                                             manufacturer='test',
                                             date_of_purchase=last_service,
                                             state=Item.AVAILABLE,
                                             serial_num='serial',
                                             description='Regulator',
                                             last_service=last_service)
        bcd = BCD.objects.create(number='1',
                                 manufacturer='test',
                                 date_of_purchase=last_service,
                                 state=Item.AVAILABLE,
                                 description='BCD',
                                 serial_num='serial',
                                 last_service=last_service,
                                 size=BCD.SMALL)
        cylinder = Cylinder.objects.create(number='1',
                                           manufacturer='test',
                                           date_of_purchase=last_service,
                                           state=Item.AVAILABLE,
                                           description='Cylinder',
                                           serial_num='123',
                                           material='steel',
                                           size=12,
                                           last_viz=last_service,
                                           last_hydro=last_service)
        bag = Item.objects.create(number='1',
                                  manufacturer='test',
                                  date_of_purchase=last_service,
                                  state=Item.AVAILABLE,
                                  description='Bag')
        bag_missing = Item.objects.create(number='1',
                                          manufacturer='test',
                                          date_of_purchase=last_service,
                                          state=Item.AVAILABLE,
                                          description='Bag')
        response = self.client.post(self.path + '/Item/', {
            f'form-0-{bag.id}': 'on',
            'form-TOTAL_FORMS': 6,
            'form-INITIAL_FORMS': 0,
            'form-MIN_NUM_FORMS': 0,
            'form-MAX_NUM_FORMS': 1000,
        })
        bag = Item.objects.get(pk=bag.id)
        missing = Item.objects.get(pk=bag_missing.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bag.state, Item.AVAILABLE)
        self.assertEqual(missing.state, Item.MISSING)
