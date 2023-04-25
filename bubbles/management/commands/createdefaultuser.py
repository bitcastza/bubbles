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
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a default super user for the system"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", default="admin", help="The username of the user."
        )
        parser.add_argument(
            "--email", default="admin@example.com", help="The email of the user."
        )
        parser.add_argument(
            "--password", default="admin", help="The password of the user."
        )
        parser.add_argument(
            "--type",
            default="superuser",
            help="Type of user to create, defaults to superuser",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(username=options["username"]).exists():
            self.stdout.write("User <{}> already exists".format(options["username"]))
            return
        self.stdout.write(
            "Creating user <{}>, password <hidden>...".format(options["username"])
        )

        if options["type"] == "superuser":
            u = User.objects.create_superuser(
                options["username"].lower(), options["email"], options["password"]
            )
        else:
            u = User.objects.create_user(
                options["username"].lower(), options["email"], options["password"]
            )
