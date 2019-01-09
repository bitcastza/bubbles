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
from django import forms

class CalendarWidget(forms.DateInput):
    def __init__(self, attrs=None, format=None):
        default_attrs = {
            'class': 'date-input',
            'width': 276
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        css = {
            'screen': ('vendor/gijgo/css/gijgo.min.css',)
        }
        js = ( 'vendor/gijgo/js/gijgo.min.js',
              'js/use_datetimepicker.js',)
