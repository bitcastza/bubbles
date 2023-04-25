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

from model_bakery import baker

from bubbles.inventory.models import BCD, Item
from bubbles.rentals import forms
from bubbles.rentals.forms import EquipmentTableWidget, RentalEquipmentListField
from bubbles.rentals.models import RentalPeriod, RentalItem, RequestItem, Rental

class StaticFunctionTest(TestCase):
    def test_get_initial_period_exists(self):
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = baker.make(RentalPeriod, start_date=start_date,
                                     end_date=end_date,
                                     hidden=False)
        self.assertEqual(forms.get_initial_period(), rental_period)

    def test_get_initial_period_none(self):
        self.assertIsNone(forms.get_initial_period())

class EquipmentTableWidgetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item = baker.make(BCD, number='1', state=BCD.AVAILABLE, description='BCD')
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = baker.make(RentalPeriod,
                                   start_date=start_date,
                                   end_date=end_date,
                                   hidden=False)
        user = User.objects.create_user(username='user')
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
        hidden_item = baker.make(Item,
                                 state = Item.AVAILABLE,
                                 hidden=True)
        context = self.table.get_context('Equipment table', None, None)
        context = context['widget']
        item_types = [x['description'] for x in context['item_types']]
        self.assertNotIn(hidden_item.description, item_types)

    def test_get_context_free(self):
        free_item = baker.make(Item,
                               state = Item.AVAILABLE,
                               free=True)
        context = self.table.get_context('Equipment table', None, None)
        context = context['widget']
        free_items = [x['description'] for x in context['free_items']]
        self.assertIn(free_item.description, free_items)


class RentalEquipmentListFieldTest(TestCase):
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

        form = RentalEquipmentListField()
        data = QueryDict(mutable=True)
        data.update({'equipment-0': self.rental_item})
        value = form.widget.value_from_datadict(data, None, 'equipment')
        self.assertIsNotNone(form.clean(value))

    def test_multiple_item_number_error(self):
        dup_item = BCD(number='1',
                       manufacturer='another',
                       date_of_purchase=datetime.date(year=2016, month=3, day=1),
                       state = BCD.AVAILABLE,
                       size = BCD.SMALL,
                       last_service=datetime.date(year=2016, month=3, day=1),
                       description='BCD')
        dup_item.save()
        form = RentalEquipmentListField()
        self.assertRaises(ValidationError, form.clean, [self.rental_item])

    def test_multple_rental_item_error(self):
        dup_item = RentalItem(item=self.item,
                             rental=self.rental,
                             cost=0)
        dup_item.save()
        form = RentalEquipmentListField()
        r = form.clean(value=[self.rental_item])
        self.assertIn(r[0], [self.rental_item, dup_item])

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

    def test_request_hood(self):
        user = User.objects.create_user(username='hood_renter')
        string = 'period={period}&belt_weight=0&{key}={description}&{key}=N/A&{key}=N/A&{key}={cost}&liability=on'.format(period=self.rental_period.pk, key='equipment-0', description=self.request_item.item_description, cost=self.request_item.cost)

        data = QueryDict(string)
        form = forms.RequestEquipmentForm(user=user,
                                          data=data)
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
        self.assertIsNotNone(form.cleaned_data['equipment'])
