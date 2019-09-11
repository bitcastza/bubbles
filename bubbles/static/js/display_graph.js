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
function sortSize(data) {
    //Order ['nXS', 'S', 'SM', 'M', 'ML', 'L', 'nXL']
    data.sort(function(a, b) {
        a = a.name;
        b = b.name;
        if (a.match(/^[\d\.]+$/) && b.match(/^[\d\.]+$/)) {
            // Compare numbers
            return a - b;
        }
        var order = ['S', 'M', 'L']
        if (a == b) return 0;
        var aLast = a.slice(-1);
        var bLast = b.slice(-1);
        var dLast = order.indexOf(aLast) - order.indexOf(bLast);
        if (dLast != 0) {
            return dLast;
        }
        // Comparing e.g. XS and S, ML and L, L and XL or 2XL and 3XL
        if (a.match(/^\d/)) {
            // a is nXS or nXL
            if (b.match(/^\d/)) {
                // so is b
                var aFirst = a.slice(0);
                var bFirst = b.slice(0);
                if (aLast == 'L') aFirst *= -1;
                if (bLast == 'L') bFirst *= -1;
                if (aFirst == bFirst) return 0;
                if (aFirst < bFirst) return -1;
                if (aFirst > bFirst) return 1;
            }
            return -1;
        }
        if (b.match(/^\d/)) {
            return 1;
        }
        // Compare XS and S, ML and L, L and XL
        if (a == 'XS') return -1;
        if (a == 'ML') return -1;
        if (a == 'L') return -1;
        return 1;
    });
}
function makeGraph(data) {
    var margin = {top: 15, right: 0, bottom: 50, left: 30}
    var goldenRatio = 1.61803;
    var totalWidth = $('#chart-view').width();
    var totalHeight = totalWidth / goldenRatio;
    if (totalHeight > $(window).height() - 150) {
        totalHeight = $(window).height() - 150;
        totalWidth = totalHeight * goldenRatio;
    }
    var width = totalWidth - margin.left - margin.right;
    var height = totalHeight - margin.top - margin.bottom;

    var xScale = d3.scaleBand()
        .range([0, width])
        .padding(0.4)
        .domain(data.map(function(d) { return d.name; }));
    var yScale = d3.scaleLinear()
        .range([height, 0])
        .domain([0, d3.max(data, function(d) { return d.value; })]);
    var g = d3.select('.chart')
        .attr('width', totalWidth)
        .attr('height', totalHeight)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    g.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(xScale).ticks(data.length));
    var dataMax = d3.max(data, function(d) { return d.value; });
    var yTicks = 10;
    console.log(dataMax);
    if (dataMax < yTicks) {
        yTicks = dataMax;
    }
    g.append('g')
        .call(d3.axisLeft(yScale).ticks(yTicks))
        .append('text')
        .attr('y', 6)
        .attr('dy', '0.71em')
        .attr('text-anchor', 'end')
        .text('value');

    var bar = g.selectAll('.bar')
        .data(data).enter()
        .append('g')
        .attr('transform', function(d, i) { return 'translate(' + xScale(d.name) + ',0)'; });

    bar.append("rect")
        .attr("class", "bar")
        .attr("y", function(d) { return yScale(d.value); })
        .attr("width", xScale.bandwidth())
        .attr("height", function(d) { return height - yScale(d.value); });
    bar.append('text')
        .attr('x', xScale.bandwidth() / 2)
        .attr('dx', function(d) { return -0.25 * (''+d.value).length + 'em'; })
        .attr('y', function(d) { return yScale(d.value) - 3; })
        .text(function(d) { return d.value; });
}

function updateGraph() {
    var type = $('#item-type').val();
    $.get('/admin/reporting/api/equipment/size/' + type,
        function(result) {
            $('#item-heading').html(type);
            data = result.sizeCount;
            sortSize(data);
            $('.chart g').remove();
            makeGraph(data);
        });
}

$(document).ready(function() {
    var data = []
    $('.result').each(function() {
        data.push({
            name: $(this).attr('id'),
            value: +$(this).attr('value')
        });
    });
    var type = $('#item-heading').text();
    $('#item-type').val(type);
    sortSize(data);
    makeGraph(data);
});
