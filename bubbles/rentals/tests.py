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
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Rental, RentalPeriod
from .views import index, rent_equipment

class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = reverse('rentals:index')
        cls.factory = RequestFactory()
        cls.request = cls.factory.get(cls.path)
        cls.user = User.objects.create_user(username='jacob')

    def test_not_logged_in(self):
        self.request.user = AnonymousUser()
        response = index(self.request)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_no_rentals(self):
        self.request.user = self.user
        
        response = index(self.request)
        self.assertNotContains(response, "rental-table")

    def test_admin_rent(self):
        user = User.objects.create_user(username='admin', is_staff=True)
        self.request.user = user
        
        response = index(self.request)
        self.assertContains(response, "Rent Equipment")

    def test_user_rent(self):
        self.request.user = self.user
        
        response = index(self.request)
        self.assertContains(response, "Request Equipment")

    def test_logged_in_rentals(self):
        self.request.user = self.user
        start_date = datetime.date(year=2018, month=7, day=2)
        end_date = start_date + datetime.timedelta(days=5)
        rental_period = RentalPeriod.objects.create(start_date=start_date,
                                                    end_date=end_date,
                                                    default_deposit=0,
                                                    default_cost_per_item=0)
        rental = Rental.objects.create(user=self.user,
                                       approved_by=self.user,
                                       state=Rental.REQUESTED,
                                       rental_period=rental_period,
                                       deposit=0)
        response = index(self.request)
        self.assertContains(response, "rental-table")

class RentEquipmentViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = reverse('rentals:request_equipment')
        cls.factory = RequestFactory()
        cls.request = cls.factory.get(cls.path)
        cls.user = User.objects.create_user(username='jacob', is_staff=True)

    def test_not_logged_in(self):
        self.request.user = AnonymousUser()
        response = rent_equipment(self.request)
        self.assertEqual(response.status_code, 302)

    def test_logged_in_not_staff(self):
        user = User.objects.create_user(username='test')
        self.request.user = user
        
        response = rent_equipment(self.request)
        self.assertEqual(response.status_code, 302)
