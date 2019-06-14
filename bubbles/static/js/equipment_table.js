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
        var enableType = $('td:first-child', $(this).parents('tr'))[0].firstChild.value;
        $('#' + enableType + '-dropdown').show();
        $(this).parents('tr').remove();
        if (!isItems()) {
            $('#submit-btn').hide();
        }
    });
}

function setTotalCost() {
    var cost = 0;
    $('.item-cost-value').each(function() {
        cost += +$(this).val();
    });
    if ($('#id_belt_weight').val() > 0) {
        cost += +$('#item-cost').text();
    }
    cost += +$('#id_deposit').val();
    $('#id_total_cost').text("R" + cost);
}

$(document).ready(function() {
    if (!isItems()) {
        $('#submit-btn').hide();
    }
    addItemRemoveListener();
    setTotalCost();
    $('.item-cost-value').on('input', setTotalCost);
    $('#id_deposit').on('input', setTotalCost);
    $('#id_belt_weight').on('input', setTotalCost);
    $('#add-dropdown a').on('click', function() {
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
            '<td class="item-description">' +
            '<input type="text" class="form-control"' +
            'name="' + description +
            '" value="' + description + '" id="' + description +
            '" readonly/>' +
            '</td>' +
            '<td class="item-size"><div class="form-group">' +
            sizeOptions +
            '</div>';
        if (showNumber) {
            cost = +$('#item-cost').text();
            if (document.getElementById('free-' + description.replace(/ /gi, '')) != null) {
                cost = 0;
            }
            row += '<td class="item-number">' +
                '<div class="form-group">' +
                '<input type="text" class="form-control" name="' + description +
                '" id="' + description + '-number"/>' +
                '</div>' +
                '</td>' +
                '<td class="item-cost">' +
                '<div class="form-group">' +
                '<input type="number" class="item-cost-value form-control" name="' +
                description +
                '" id="' + description + '-cost" value="' + cost + '" min="0"/>' +
                '</div>' +
                '</td>';
        }
        row += '<td class="item-entry">' +
            '<a href="#"><i class="fas fa-minus item-remove"></i></a>'+
            '</td>' +
            '</tr>';
        $('#equipment-table > tbody:last-child').append(row);
        $('#submit-btn').show();
        $('.item-cost-value').on('input', setTotalCost);
        setTotalCost();
        if (! showNumber) {
            $('#' + description + '-dropdown').hide();
        }
        addItemRemoveListener();
    });
});
