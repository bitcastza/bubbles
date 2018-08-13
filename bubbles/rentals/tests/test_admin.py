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

from django.contrib import admin
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from bubbles.inventory.models import Item
from bubbles.rentals.admin import *
from bubbles.rentals.models import Rental, RentalPeriod, RentalItem, RequestItem

class RentalAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.start_date = datetime.date(year=2018, month=7, day=2)
        cls.end_date = cls.start_date + datetime.timedelta(days=5)
        user = User.objects.create_user(username='jacob')
        rental_period = RentalPeriod.objects.create(start_date=cls.start_date,
                                                    end_date=cls.end_date,
                                                    default_deposit=0,
                                                    default_cost_per_item=0)
        cls.rental = Rental.objects.create(user=user,
                                           approved_by=user,
                                           state=Rental.REQUESTED,
                                           rental_period=rental_period,
                                           deposit=0)
        cls.rental_admin = RentalAdmin(Rental, admin.sites.site)

    def test_start_date(self):
        self.assertEqual(self.rental_admin.start_date(self.rental), self.start_date)

    def test_end_date(self):
        self.assertEqual(self.rental_admin.end_date(self.rental), self.end_date)

class RentalAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        user = User.objects.create_user(username='jacob')
        cls.rental_period = RentalPeriod.objects.create(start_date=start_date,
                                                        end_date=end_date,
                                                        default_deposit=100,
                                                        default_cost_per_item=25)
        cls.admin = RentalPeriodAdmin(RentalPeriod, admin.sites.site)

    def test_deposit(self):
        self.assertEqual(self.admin.deposit(self.rental_period),
                         "R{}".format(self.rental_period.default_deposit))

    def test_cost_per_item(self):
        self.assertEqual(self.admin.cost_per_item(self.rental_period),
                         "R{}".format(self.rental_period.default_cost_per_item))

class RentalItemAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        cls.user = User.objects.create_user(username='jacob')
        rental_period = RentalPeriod.objects.create(start_date=start_date,
                                                    end_date=end_date,
                                                    default_deposit=100,
                                                    default_cost_per_item=25)
        rental = Rental.objects.create(user=cls.user,
                                       approved_by=cls.user,
                                       state=Rental.REQUESTED,
                                       rental_period=rental_period,
                                       deposit=0)
        cls.item = Item(number="1",
                        manufacturer="test",
                        date_of_purchase=start_date,
                        state = Item.AVAILABLE,
                        description="Test item")
        cls.rental_item = RentalItem(rental=rental, item=cls.item, cost=25)
        cls.admin = RentalItemAdmin(RentalItem, admin.sites.site)

    def test_number(self):
        self.assertEqual(self.admin.number(self.rental_item),
                         self.item.number)

    def test_description(self):
        self.assertEqual(self.admin.description(self.rental_item),
                         self.item.description)

    def test_user_rental_null(self):
        self.rental_item.rental = None
        self.assertIsNone(self.admin.user(self.rental_item))

    def test_user(self):
        self.assertEqual(self.admin.user(self.rental_item),
                         self.user)

class RequestItemAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        cls.user = User.objects.create_user(username='jacob')
        rental_period = RentalPeriod.objects.create(start_date=start_date,
                                                    end_date=end_date,
                                                    default_deposit=100,
                                                    default_cost_per_item=25)
        rental = Rental.objects.create(user=cls.user,
                                       approved_by=cls.user,
                                       state=Rental.REQUESTED,
                                       rental_period=rental_period,
                                       deposit=0)
        cls.request_item = RequestItem(rental=rental,
                              item_description="Test description",
                              item_size="M",
                              cost=25)
        cls.admin = RequestItemAdmin(RequestItem, admin.sites.site)

    def test_number(self):
        self.assertEqual(self.admin.size(self.request_item),
                         self.request_item.item_size)

    def test_description(self):
        self.assertEqual(self.admin.description(self.request_item),
                         self.request_item.item_description)

    def test_user_rental_null(self):
        self.request_item.rental = None
        self.assertIsNone(self.admin.user(self.request_item))

    def test_user(self):
        self.assertEqual(self.admin.user(self.request_item),
                         self.user)
