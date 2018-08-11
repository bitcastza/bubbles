/*
 * Bubbles is Copyright (C) 2018 Kyle Robbertze <krobbertze@gmail.com>
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

function isItems() {
    var numItems = $('.item-entry').length;
    return numItems > 0;
}

// TODO: Does not re-add the item to the dropdown after it is removed
function addItemRemoveListener() {
    $('.item-remove').on('click', function() {
        var enableType = $('td:first-child', $(this).parents('tr')).val();
        $('#' + enableType + '-dropdown').show();
        $(this).parents('tr').remove();
        if (!isItems()) {
            $('#submit-btn').hide();
        }
    });
}

$(document).ready(function() {
    if (!isItems()) {
        $('#submit-btn').hide();
    }
    addItemRemoveListener();
    $('#add-dropdown li').on('click', function() {
        var currentItem = this;
        var description = $(currentItem).text();
        var sizeOptions = '<input type="text" '+
            'class="form-control" id="' + description +
            '-size" name="' + description + '" value="N/A" readonly>';
        $('#size-options').children('div').each(function() {
            if (this.id != description) {
                return;
            }
            if ($(this).is(':empty')) {
                sizeOptions = '<select class="form-control disabled" id="' +
                    description + '-size" name="' + description + '"/>';
            } else {
                sizeOptions = '<select class="form-control" id="' +
                    description + '-size" name="' +
                    description + '">';
                $('#' + this.id + ' .sizes li').each(function() {
                    sizeOptions += '<option>' + $(this).text() + '</option>';
                });
                sizeOptions += '</select>';
            }
        });
        var description = $(this).text();
        var showNumber = $('#show-number').text() == "True";
        var row = '<tr>' +
            '<td>' +
            '<input type="text" class="form-control" name="' + description +
            '" value="' + description + '" id="' + description +
            '" readonly/>' +
            '</td>' +
            '<td class="size"><div class="form-group">' +
            sizeOptions +
            '</div>';
        if (showNumber) {
            cost = $('#item-cost').text();
            row += '<td>' +
                '<div class="form-group">' +
                '<input type="text" class="form-control" name="' + description +
                '" id="' + description + '-number"/>' +
                '</div>' +
                '</td>' +
                '<td>' +
                '<div class="form-group">' +
                '<input type="number" class="form-control" name="' + description +
                '" id="' + description + '-cost" value="' + cost + '" min="0"/>' +
                '</div>' +
                '</td>';
        }
        row += '<td class="item-entry">' +
            '<a href="#"><i class="glyphicon glyphicon-remove item-remove"></i></a>'+
            '</td>' +
            '</tr>';
        $('#equipment-table > tbody:last-child').append(row);
        $('#submit-btn').show();
        if (! showNumber) {
            $('#' + description + '-dropdown').hide();
        }
        addItemRemoveListener();
    });
});
