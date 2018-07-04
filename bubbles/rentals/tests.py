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

from .models import Rental
from .views import index

class RentalTests(TestCase):
    def test_get_due_date(self):
        renter = User.objects.create(username='test')
        start_date = datetime.date(year=2018, month=7, day=2)
        duration = datetime.timedelta(days=5)
        rental = Rental.objects.create(user=renter,
                                       start_date=start_date,
                                       period=duration,
                                       deposit=0)
        self.assertEqual(rental.get_end_date(), start_date + duration)

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
        duration = datetime.timedelta(days=5)
        rental = Rental.objects.create(user=self.user,
                                       start_date=start_date,
                                       period=duration,
                                       deposit=0)
        response = index(self.request)
        self.assertContains(response, "rental-table")
