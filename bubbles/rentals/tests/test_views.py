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

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from model_bakery import baker

from bubbles.rentals.models import Rental, RentalPeriod, RentalItem, RequestItem
from bubbles.rentals.views import (
    index,
    rent_equipment,
    request_equipment,
    save_rental_request,
    return_equipment,
)
from bubbles.inventory.models import Item, BCD, Weight


class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = reverse("rentals:index")
        cls.factory = RequestFactory()
        cls.request = cls.factory.get(cls.path)
        cls.user = User.objects.create_user(username="jacob")

    def test_not_logged_in(self):
        self.request.user = AnonymousUser()
        response = index(self.request)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_no_rentals(self):
        self.request.user = self.user

        response = index(self.request)
        self.assertNotContains(response, "rental-table")

    def test_admin_rent(self):
        user = User.objects.create_user(username="admin", is_staff=True)
        self.request.user = user

        response = index(self.request)
        self.assertContains(response, "Rent Equipment")

    def test_user_rent(self):
        self.request.user = self.user

        response = index(self.request)
        self.assertContains(response, "Request Equipment")

    def test_logged_in_rentals(self):
        self.request.user = self.user
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=5)
        item = Item.objects.create(
            number="1",
            manufacturer="test",
            date_of_purchase=datetime.date.today(),
            state=Item.IN_USE,
            description="BCD",
        )
        rental_period = RentalPeriod.objects.create(
            start_date=start_date,
            end_date=end_date,
            default_deposit=0,
            default_cost_per_item=0,
            name="Test",
        )
        rental = Rental.objects.create(
            user=self.user,
            approved_by=self.user,
            state=Rental.REQUESTED,
            rental_period=rental_period,
            deposit=0,
        )
        RentalItem.objects.create(rental=rental, item=item, cost=25)
        response = index(self.request)
        self.assertContains(response, "rental-table")


class RequestEquipmentViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = reverse("rentals:request_equipment")
        cls.factory = RequestFactory()
        cls.request = cls.factory.get(cls.path)
        cls.user = User.objects.create_user(username="jacob", is_staff=False)

    def test_not_logged_in(self):
        self.request.user = AnonymousUser()
        response = request_equipment(self.request)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_not_exist(self):
        self.request.user = self.user

        self.assertRaisesMessage(
            Http404, "", request_equipment, request=self.request, request_id=1
        )

    def test_logged_in_not_own(self):
        self.request.user = self.user
        other_user = User.objects.create_user(username="other")
        rental_period = RentalPeriod.objects.create(
            start_date=datetime.date.today(),
            end_date=datetime.date.today(),
            default_deposit=0,
            default_cost_per_item=0,
            name="Test",
        )
        rental = Rental.objects.create(
            user=other_user,
            state=Rental.REQUESTED,
            rental_period=rental_period,
            deposit=0,
        )

        self.assertRaisesMessage(
            PermissionDenied,
            "",
            request_equipment,
            request=self.request,
            request_id=rental.id,
        )

    def test_request_equipment_post(self):
        start_date = datetime.date.today()
        rental_period = baker.make(
            RentalPeriod,
            start_date=start_date,
            end_date=start_date + datetime.timedelta(days=5),
            hidden=False,
        )

        bcd = baker.make(BCD, number="1", size=BCD.MEDIUM)
        item = baker.make(Item, number="2")
        request_data = {
            "period": rental_period.id,
            "belt_weight": 0,
            "equipment-0": [
                bcd.description,
                bcd.size,
                "N/A",
                30,
            ],
            "equipment-1": [
                item.description,
                "N/A",
                "N/A",
                -1,
            ],
            "liability": "on",
        }
        request = self.factory.post(self.path, request_data)
        request.user = self.user
        response = request_equipment(request)
        self.assertEqual(response.status_code, 302)
        rental_request = Rental.objects.get(user=self.user, rental_period=rental_period)
        request_items = rental_request.requestitem_set
        self.assertEqual(len(request_items.all()), 2)
        bcd_request = request_items.get(item_description=bcd.description)
        self.assertEqual(bcd_request.cost, rental_period.default_cost_per_item)
        self.assertEqual(bcd_request.item_size, bcd.size)
        item_request = request_items.get(item_description=item.description)
        self.assertEqual(item_request.cost, rental_period.default_cost_per_item)
        self.assertIsNone(item_request.item_size)

    def test_save_request_equipment_post(self):
        start_date = datetime.date.today()
        rental_period = baker.make(
            RentalPeriod,
            start_date=start_date,
            end_date=start_date + datetime.timedelta(days=5),
            hidden=False,
        )
        rental = baker.make(Rental, state=Rental.REQUESTED, rental_period=rental_period)

        bcd = baker.make(BCD, number="1")
        item = baker.make(Item, number="2")
        request_data = {
            "period": rental_period.id,
            "belt_weight": 0,
            "equipment-0": [
                bcd.description,
                bcd.size,
                bcd.number,
                30,
            ],
            "equipment-1": [
                item.description,
                "N/A",
                item.number,
                -1,
            ],
        }
        path = reverse("rentals:save_rental_request", args=(rental.id,))
        request = self.factory.post(path, request_data)
        request.user = self.user
        response = save_rental_request(request, rental.id)
        self.assertEqual(response.status_code, 302)
        request_items = rental.requestitem_set
        self.assertEqual(len(request_items.all()), 2)
        bcd_request = request_items.get(item_description=bcd.description)
        self.assertEqual(bcd.number, bcd_request.item_number)
        self.assertEqual(bcd_request.cost, rental_period.default_cost_per_item)
        self.assertEqual(bcd_request.item_size, bcd.size)
        item_request = request_items.get(item_description=item.description)
        self.assertEqual(item.number, item_request.item_number)
        self.assertEqual(item_request.cost, rental_period.default_cost_per_item)
        self.assertIsNone(item_request.item_size)


class RentEquipmentViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = reverse("rentals:rent_equipment")
        cls.factory = RequestFactory()
        cls.request = cls.factory.get(cls.path)
        cls.user = User.objects.create_user(username="jacob", is_staff=True)

    def test_not_logged_in(self):
        self.request.user = AnonymousUser()
        response = rent_equipment(self.request)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_not_staff(self):
        user = User.objects.create_user(username="test")
        self.request.user = user

        response = rent_equipment(self.request)
        self.assertEqual(response.status_code, 302)

    def test_get_rental_form_with_rental_request(self):
        self.request.user = self.user
        rental = baker.make(Rental)
        description = ["Regulator", "Cylinder", "Hood"]
        request_items = [
            baker.make(RequestItem, rental=rental, item_description=description[i])
            for i in range(3)
        ]
        request_items[1].item_number = "1"
        request_items[1].save()
        response = rent_equipment(self.request, rental.id)
        for item in request_items:
            self.assertContains(response, item.item_description)
        self.assertContains(
            response,
            f'<input type="text" class="form-control" name="equipment-0" value="" id="{description[0]}-number"/>',
            html=True,
        )
        self.assertContains(
            response,
            f'<input type="text" class="form-control" name="equipment-1" value="1" id="{description[1]}-number"/>',
            html=True,
        )

    def test_rent_equipment_post(self):
        Weight.objects.create(total_weight=50, available_weight=50)
        start_date = datetime.date.today()
        rental_period = baker.make(
            RentalPeriod,
            start_date=start_date,
            end_date=start_date + datetime.timedelta(days=5),
            hidden=False,
        )
        rental = baker.make(Rental, state=Rental.REQUESTED, rental_period=rental_period)

        bcd = baker.make(BCD, description="BCD", number="1", state=Item.AVAILABLE)
        item = baker.make(Item, number="2", state=Item.AVAILABLE)
        request_data = {
            "period": rental.rental_period.id,
            "belt_weight": 5,
            "equipment-0": [
                bcd.description,
                bcd.size,
                bcd.number,
                "30",
            ],
            "equipment-1": [
                item.description,
                "N/A",
                item.number,
                "0",
            ],
            "deposit": "100",
        }
        request = self.factory.post(self.path, request_data)
        request.user = self.user
        response = rent_equipment(request, rental.id)
        rental.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(rental.rentalitem_set.all()), 2)
        self.assertEqual(len(rental.requestitem_set.all()), 0)
        self.assertEqual(rental.state, Rental.RENTED)
        weight = Weight.objects.first()
        self.assertEqual(weight.total_weight - weight.available_weight, 5)

    def test_get_return_form_with_rental_request(self):
        self.request.user = self.user
        start_date = datetime.date.today()
        rental_period = baker.make(
            RentalPeriod,
            start_date=start_date,
            end_date=start_date + datetime.timedelta(days=5),
            hidden=False,
        )
        rental = baker.make(Rental, rental_period=rental_period)
        bcd = baker.make(BCD, description="BCD", number="1", state=Item.IN_USE)
        baker.make(RentalItem, item=bcd, rental=rental)
        item = baker.make(Item, number="2", state=Item.IN_USE)
        baker.make(RentalItem, item=item, rental=rental)
        response = return_equipment(self.request, rental.id)
        self.assertContains(response, bcd.description)
        self.assertContains(response, item.description)
        self.assertContains(
            response,
            f'<input type="text" class="form-control" name="equipment-0" value="{bcd.description}" id="{bcd.description}-description" readonly/>',
            html=True,
        )
        self.assertContains(
            response,
            f'<input type="text" class="form-control" name="equipment-1" value="{item.number}" id="{item.description}-number"/>',
            html=True,
        )
        self.assertContains(
            response,
            f'<select class="form-control" id="{bcd.description}-size" name="equipment-0">',
            html=True,
        )

    def test_return_equipment_post(self):
        Weight.objects.create(total_weight=50, available_weight=45)
        start_date = datetime.date.today()
        rental_period = baker.make(
            RentalPeriod,
            start_date=start_date,
            end_date=start_date + datetime.timedelta(days=5),
            hidden=False,
        )
        rental = baker.make(Rental, state=Rental.RENTED, rental_period=rental_period)

        bcd = baker.make(BCD, description="BCD", number="1", state=Item.IN_USE)
        baker.make(RentalItem, item=bcd, rental=rental)
        item = baker.make(Item, number="2", state=Item.IN_USE)
        baker.make(RentalItem, item=item, rental=rental)
        request_data = {
            "period": rental.rental_period.id,
            "belt_weight": 5,
            "equipment-0": [
                bcd.description,
                bcd.size,
                bcd.number,
                "",
            ],
            "equipment-1": [
                item.description,
                "N/A",
                item.number,
                "",
            ],
            "deposit": "100",
        }
        path = reverse("rentals:return_equipment", args=(rental.id,))
        request = self.factory.post(path, request_data)
        request.user = self.user
        response = return_equipment(request, rental.id)
        rental.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(rental.rentalitem_set.all()), 2)
        for item in rental.rentalitem_set.all():
            self.assertEqual(item.item.state, Item.AVAILABLE)
        self.assertEqual(len(rental.requestitem_set.all()), 0)
        self.assertEqual(rental.state, Rental.RETURNED)
        weight = Weight.objects.first()
        self.assertEqual(weight.total_weight - weight.available_weight, 0)
