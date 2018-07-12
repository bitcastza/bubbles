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
        currentItem = this;
        var sizeOptions = "N/A";
        $('#size-options').children('div').each(function() {
            if (this.id != $(currentItem).text()) {
                return;
            }
            if ($(this).is(':empty')) {
                sizeOptions = '<select class="form-control disabled" id="' +
                    $(currentItem).text() + '-size"/>';
            } else {
                sizeOptions = '<select class="form-control" id="' +
                    $(currentItem).text() + '-size">';
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
            '<td><div class="form-group">' +
            sizeOptions +
            '</div>';
        if (showNumber) {
            row += '<td>' +
                '<div class="form-group">' +
                '<input type="text" class="form-control" name="' + description +
                '" id="' + description + '-number"/>' +
                '</div>' +
                '</td>' +
                '<td>' +
                '<div class="form-group">' +
                '<div class="input-group-prepend">' +
                '<span class="input-group-text">R</span>' +
                '</div>' +
                '<input type="text" class="form-control" name="' + description +
                '" id="' + description + '-cost"/>' +
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
