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

from bubbles.inventory.models import Item
from bubbles.rentals.models import Rental, RentalPeriod, RentalItem, RequestItem


class RentalPeriodTest(TestCase):
    def test_str(self):
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = RentalPeriod(
            start_date=start_date,
            end_date=end_date,
            default_deposit=100,
            default_cost_per_item=25,
            name="Test",
            hidden=False,
        )
        self.assertEqual(
            rental_period.__str__(), "{} ({} - {})".format("Test", start_date, end_date)
        )


class RentalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        cls.rental_period = RentalPeriod(
            start_date=start_date,
            end_date=end_date,
            default_deposit=100,
            default_cost_per_item=25,
            name="Test",
            hidden=False,
        )
        cls.user = User.objects.create_user(username="jacob")
        cls.rental = Rental(
            user=cls.user,
            state=Rental.REQUESTED,
            deposit=100,
            rental_period=cls.rental_period,
        )

    def test_overdue_staff(self):
        self.rental_period.end_date = None
        self.assertFalse(self.rental.is_overdue())

    def test_overdue_true(self):
        today = datetime.date.today()
        self.rental_period.end_date = today - datetime.timedelta(days=1)
        self.assertTrue(self.rental.is_overdue())

    def test_overdue_false(self):
        today = datetime.date.today()
        self.rental_period.end_date = today + datetime.timedelta(days=1)
        self.assertFalse(self.rental.is_overdue())

    def test_due_staff(self):
        self.rental_period.end_date = None
        self.assertFalse(self.rental.is_due())

    def test_due_true(self):
        today = datetime.date.today()
        self.rental_period.end_date = today
        self.assertTrue(self.rental.is_due())

    def test_due_false_coming(self):
        today = datetime.date.today()
        self.rental_period.end_date = today + datetime.timedelta(days=1)
        self.assertFalse(self.rental.is_due())

    def test_due_false_past(self):
        today = datetime.date.today()
        self.rental_period.end_date = today - datetime.timedelta(days=1)
        self.assertFalse(self.rental.is_due())

    def test_str(self):
        self.assertEqual(
            self.rental.__str__(),
            f"Rental by {self.user} for {self.rental_period}",
        )


class RentalItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = RentalPeriod(
            start_date=start_date,
            end_date=end_date,
            default_deposit=100,
            default_cost_per_item=25,
            name="Test",
            hidden=False,
        )
        cls.user = User.objects.create_user(username="jacob")
        rental = Rental(
            user=cls.user,
            state=Rental.REQUESTED,
            deposit=100,
            rental_period=rental_period,
        )
        cls.item = Item(
            number="1",
            manufacturer="test",
            date_of_purchase=start_date,
            state=Item.AVAILABLE,
            description="Test item",
        )
        cls.rental_item = RentalItem(rental=rental, item=cls.item, cost=25)

    def test_str_no_rental(self):
        self.rental_item.rental = None
        self.assertEqual(self.rental_item.__str__(), f"{self.item} to unknown")

    def test_str(self):
        self.assertEqual(self.rental_item.__str__(), f"{self.item} to {self.user}")

    def test_eq_different_type(self):
        self.assertFalse(self.rental_item.__eq__("Test"))

    def test_eq(self):
        self.assertTrue(self.rental_item.__eq__(self.rental_item))


class RentalItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = RentalPeriod(
            start_date=start_date,
            end_date=end_date,
            default_deposit=100,
            default_cost_per_item=25,
            name="Test",
            hidden=False,
        )
        cls.user = User.objects.create_user(username="jacob")
        rental = Rental(
            user=cls.user,
            state=Rental.REQUESTED,
            deposit=100,
            rental_period=rental_period,
        )
        cls.item_description = "Test request item"
        cls.request_item = RequestItem(
            rental=rental, item_description=cls.item_description, item_size="M", cost=25
        )

    def test_str_no_rental(self):
        self.request_item.rental = None
        self.assertEqual(
            self.request_item.__str__(), f"{self.item_description} to unknown"
        )

    def test_str(self):
        self.assertEqual(
            self.request_item.__str__(), f"{self.item_description} to {self.user}"
        )

    def test_eq(self):
        self.assertTrue(self.request_item.__eq__(self.request_item))
