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

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

class BubblesAdminSite(admin.AdminSite):
    index_title = None
    index_template = 'admin/bubbles/index.html'
    app_index_template = 'admin/bubbles/index.html'

    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        extra_context = extra_context or {}
        return super(BubblesAdminSite, self).index(request, extra_context=extra_context)

    def each_context(self, request):
        context = super(BubblesAdminSite, self).each_context(request)
        context['apps_length'] = len(self.get_app_list(request))
        return context

admin_site = BubblesAdminSite(name='Bubbles Administration')
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
