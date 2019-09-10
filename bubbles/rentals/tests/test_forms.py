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
from django.forms import ValidationError
from django.test import TestCase
from django.http.request import QueryDict

from bubbles.inventory.models import BCD, Item
from bubbles.rentals import forms
from bubbles.rentals.forms import EquipmentTableWidget, EquipmentListField
from bubbles.rentals.models import RentalPeriod, RentalItem, RequestItem, Rental

class StaticFunctionTest(TestCase):
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
        item_size_map = {self.item.description: [self.item.size],
                         'Booties': [],
                         'Cylinder': [],
                         'Fins': [],
                         'Wetsuit': [],}
        context = context['widget']
        self.assertEqual(context['item_size_map'], item_size_map)
        item_types = [x['description'] for x in context['item_types']]
        self.assertIn(self.item.description, item_types)

    def test_get_context_hidden(self):
        hidden_item = Item(number='3',
                           manufacturer='Reef',
                           date_of_purchase=datetime.date(year=2015,
                                                          month=1,
                                                          day=1),
                           state = Item.AVAILABLE,
                           description='Hood',
                           hidden=True)
        hidden_item.save()
        context = self.table.get_context('Equipment table', None, None)
        context = context['widget']
        item_types = [x['description'] for x in context['item_types']]
        self.assertNotIn(hidden_item.description, item_types)

    def test_get_context_free(self):
        free_item = Item(number='3',
                           manufacturer='Reef',
                           date_of_purchase=datetime.date(year=2015,
                                                          month=1,
                                                          day=1),
                           state = Item.AVAILABLE,
                           description='Hood',
                           free=True)
        free_item.save()
        context = self.table.get_context('Equipment table', None, None)
        context = context['widget']
        free_items = [x['description'] for x in context['free_items']]
        self.assertIn(free_item.description, free_items)

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

class EquipmentListFieldTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = BCD(number='1',
                   manufacturer='test',
                   date_of_purchase=datetime.date(year=2016, month=3, day=1),
                   state = BCD.AVAILABLE,
                   size = BCD.LARGE,
                   last_service=datetime.date(year=2016, month=3, day=1),
                   description='BCD')
        cls.item.save()
        start_date = datetime.date.today()
        rental_period = RentalPeriod(start_date=start_date,
                                     end_date=start_date + datetime.timedelta(days=5),
                                     default_deposit=100,
                                     default_cost_per_item=25,
                                     name='Test',
                                     hidden=False)
        rental_period.save()
        user = User.objects.create_user(username='jacob')
        cls.rental = Rental(rental_period=rental_period,
                        user=user,
                        state=Rental.RENTED,
                        deposit=0)
        cls.rental.save()
        cls.rental_item = RentalItem(item=cls.item,
                                          rental=cls.rental,
                                          cost=0)
        cls.rental_item.save()

    def test_return_rented_item_after_second_rental(self):
        start_date = datetime.date(year=2018, month=3, day=1)
        returned_rental_period = RentalPeriod(start_date=start_date,
                                     end_date=start_date + datetime.timedelta(days=4),
                                     default_deposit=100,
                                     default_cost_per_item=25,
                                     name='Test',
                                     hidden=False)
        returned_rental_period.save()
        user = User.objects.create_user(username='bob')
        returned_rental = Rental(rental_period=returned_rental_period,
                        user=user,
                        state=Rental.RETURNED,
                        deposit=0)
        returned_rental.save()
        returned_rental_item = RentalItem(item=self.item,
                                          rental=returned_rental,
                                          cost=0,
                                          returned=True)
        returned_rental_item.save()

        form = EquipmentListField(show_number=True)
        data = {
            'equipment': [self.rental_item],
        }
        form.widget.value_from_datadict(data, None, 'equipment')
        self.assertIsNotNone(form.clean("Test"))

    def test_multiple_item_number_error(self):
        dup_item = BCD(number='1',
                       manufacturer='another',
                       date_of_purchase=datetime.date(year=2016, month=3, day=1),
                       state = BCD.AVAILABLE,
                       size = BCD.SMALL,
                       last_service=datetime.date(year=2016, month=3, day=1),
                       description='BCD')
        dup_item.save()
        form = EquipmentListField(show_number=True)
        data = {
            'equipment': [self.rental_item],
        }
        form.widget.value_from_datadict(data, None, 'equipment')
        self.assertRaises(ValidationError, form.clean, 'Test')

class EquipmentFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = Item(number='3',
                   manufacturer='Reef',
                   date_of_purchase=datetime.date(year=2015, month=1, day=1),
                   state = Item.AVAILABLE,
                   description='Hood')
        cls.item.save()
        cls.request_item = RequestItem(item_description=cls.item.description,
                                       cost=25)
        start_date = datetime.date.today()
        cls.rental_period = RentalPeriod(start_date=start_date,
                                     end_date=start_date + datetime.timedelta(days=5),
                                     default_deposit=100,
                                     default_cost_per_item=25,
                                     name='Test',
                                     hidden=False)
        cls.rental_period.save()
        cls.user = User.objects.create_user(username='jacob')
        cls.rental = Rental(rental_period=cls.rental_period,
                        user=cls.user,
                        state=Rental.REQUESTED,
                        deposit=0)
        cls.rental.save()

    def test_request_hood(self):
        string = 'period={period}&belt_weight=0&{key}={key}&{key}=N/A&liability=on'.format(period=self.rental_period, key=self.request_item.item_description)
        data = QueryDict(string)
        form = forms.RequestEquipmentForm(user=self.user,
                                          data=data)
        form.clean()
        self.assertIsNotNone(form.cleaned_data['equipment'])
