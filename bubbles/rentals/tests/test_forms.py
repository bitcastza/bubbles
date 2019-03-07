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
from django.test import TestCase
from django.http.request import QueryDict

from bubbles.inventory.models import BCD
from bubbles.rentals import forms
from bubbles.rentals.forms import EquipmentTableWidget, EquipmentListField
from bubbles.rentals.models import RentalPeriod, RentalItem, RequestItem, Rental

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
        results = forms.get_sizes(BCD)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], BCD.LARGE)

    def test_get_sizes_none(self):
        results = forms.get_sizes(BCD)
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
        item_size_map = forms.get_item_size_map()
        self.assertEqual(len(item_size_map['BCD']), 1)
        self.assertEqual(len(item_size_map['Booties']), 0)

    def test_get_initial_period_exists(self):
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = RentalPeriod(start_date=start_date,
                                     end_date=end_date,
                                     default_deposit=100,
                                     default_cost_per_item=25,
                                     name='Test',
                                     hidden=False)
        rental_period.save()
        self.assertEqual(forms.get_initial_period(), rental_period)

    def test_get_initial_period_none(self):
        self.assertIsNone(forms.get_initial_period())

class EquipmentTableWidgetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        date_of_purchase = datetime.date(year=2018, month=7, day=2)
        cls.item = BCD(number='1',
                   manufacturer='test',
                   date_of_purchase=date_of_purchase,
                   state = BCD.AVAILABLE,
                   size = BCD.LARGE,
                   last_service=date_of_purchase,
                   description='BCD')
        cls.item.save()
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = RentalPeriod(start_date=start_date,
                                     end_date=end_date,
                                     default_deposit=100,
                                     default_cost_per_item=25,
                                     name='Test',
                                     hidden=False)
        user = User.objects.create_user(username='jacob')
        cls.rental = Rental(rental_period=rental_period,
                            user=user,
                            state=Rental.REQUESTED,
                            deposit=0)
        cls.table = EquipmentTableWidget()
        cls.table.show_number = True

    def test_get_context(self):
        context = self.table.get_context('Equipment table', None, None)
        item_size_map = {'BCD': [BCD.LARGE], 
                         'Booties': [],
                         'Cylinder': [],
                         'Fins': [],
                         'Wetsuit': [],}
        self.assertEqual(context['widget']['item_size_map'], item_size_map)
        self.assertEqual(context['widget']['item_types'][0]['description'], 'BCD')

    def test_value_from_datadict_rental_items(self):
        item = RentalItem(item=self.item,
                          rental=self.rental,
                          cost=0)
        data = {'equipment': [item,]}
        self.table.value_from_datadict(data, None, 'equipment')
        self.assertEqual(len(self.table.widgets), 1)
        self.assertEqual(self.table.widgets[0].item_description, self.item.description)

    def test_value_from_datadict_request_item(self):
        item = RequestItem(rental=self.rental,
                           item_description=self.item.description,
                           item_size=self.item.size,
                           cost=self.rental.rental_period.default_cost_per_item)
        data = {'equipment': [item,]}
        self.table.value_from_datadict(data, None, 'equipment')
        self.assertEqual(len(self.table.widgets), 1)
        self.assertEqual(self.table.widgets[0].item_description,
                         item.item_description)

    def test_value_from_datadict_rental_post_cost(self):
        string = 'r=test&r=two&{key}={key}&{key}={size}&{key}={number}&{key}=0'.format(
            key=self.item.description,
            size=self.item.size,
            number=self.item.number)
        data = QueryDict(string)
        self.table.show_number = True
        self.table.show_cost = True
        self.table.value_from_datadict(data, None, 'equipment')
        self.assertEqual(len(self.table.widgets), 1)
        self.assertEqual(self.table.widgets[0].item_description,
                         self.item.description)

    def test_value_from_datadict_rental_post(self):
        string = 'r=test&r=two&{key}={key}&{key}={size}'.format(
            key=self.item.description,
            size=self.item.size)
        data = QueryDict(string)
        self.table.show_number = False
        self.table.value_from_datadict(data, None, 'equipment')
        self.assertEqual(len(self.table.widgets), 1)
        self.assertEqual(self.table.widgets[0].item_description,
                         self.item.description)
