/*
 * Bubbles is Copyright (C) 2018-2019 Kyle Robbertze <kyle@paddatrapper.com>
 *
 * Bubbles is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 as
 * published by the Free Software Foundation.
 *
 * Bubbles is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Bubbles. If not, see <http://www.gnu.org/licenses/>.
 */
$(document).ready(function() {
    var form = document.getElementById('rental-form')
    var defaultAction = form.action;

    document.getElementById('submit-btn').onclick = function() {
        form.action = defaultAction;
        form.submit();
    };

    document.getElementById('save-btn').onclick = function() {
        var action = $('#save-target').text();
        form.action = action;
        form.submit();
    };
});
