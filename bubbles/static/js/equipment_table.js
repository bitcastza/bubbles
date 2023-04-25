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
 const
 * You should have received a copy of the GNU General Public License
 * along with Bubbles. If not, see <http://www.gnu.org/licenses/>.
 */

function isItems() {
  var numItems = $(".item-entry").length;
  return numItems > 0;
}

function addItemRemoveListener() {
  $(".item-remove").on("click", function () {
    var enableType = $("td:first-child", $(this).parents("tr"))[0].firstChild
      .value;
    $("#" + enableType + "-dropdown").show();
    $(this).parents("tr").remove();
    if (!isItems()) {
      $("#submit-btn").hide();
    }
  });
}

function setTotalCost() {
  var cost = 0;
  $(".item-cost-value").each(function () {
    cost += +$(this).val();
  });
  if ($("#id_belt_weight").val() > 0) {
    cost += +$("#item-cost").text();
  }
  cost += +$("#id_deposit").val();
  $("#id_total_cost").text("R" + cost);
}

$(document).ready(function () {
  if (!isItems()) {
    $("#submit-btn").hide();
  }
  addItemRemoveListener();
  setTotalCost();
  $(".item-cost-value").on("input", setTotalCost);
  $("#id_deposit").on("input", setTotalCost);
  $("#id_belt_weight").on("input", setTotalCost);
  $("#add-dropdown a").on("click", function () {
    const currentItem = this;
    const description = $(currentItem).text();
    const fieldName = $(".equipment-table")[0].id;
    const currentNumber = $("#" + fieldName + " tbody tr").length;
    const namePrefix = fieldName + "-" + currentNumber;
    var sizeOptions = $(document.createElement("input"))
      .attr({
        type: "text",
        id: description + "-size",
        name: namePrefix,
        value: "N/A",
        readonly: true,
      })
      .addClass("form-control");
    $("#size-options")
      .children("div")
      .each(function () {
        if (this.id != description) {
          return;
        }
        if ($(this).is(":empty")) {
          sizeOptions = $(document.createElement("select"))
            .addClass("form-control")
            .addClass("disabled")
            .attr({ id: description + "-size", name: namePrefix });
        } else {
          sizeOptions = $(document.createElement("select"))
            .addClass("form-control")
            .attr({ id: description + "-size", name: namePrefix });
          $("#" + this.id + " .sizes li").each(function () {
            var option = $(document.createElement("option")).append(
              $(this).text()
            );
            sizeOptions.append(option);
          });
        }
      });
    var showNumber = $("#show-number").text() == "True";
    var itemDescription = $(document.createElement("td")).addClass(
      "item-description"
    );
    itemDescription.append(
      $(document.createElement("input"))
        .addClass("form-control")
        .attr({
          type: "text",
          name: namePrefix,
          value: description,
          id: description + "-description",
          readonly: "",
        })
    );
    var itemSize = $(document.createElement("td"))
      .addClass("item-size")
      .append(sizeOptions);
    var row = $(document.createElement("tr"))
      .append(itemDescription)
      .append(itemSize);

    var itemNumber = $(document.createElement("td")).addClass("item-number");
    var itemNumberInput = $(document.createElement("input"))
      .addClass("form-control")
      .attr({
        type: "text",
        name: namePrefix,
        id: description + "-number",
      });

    var itemCost = $(document.createElement("td")).addClass("item-cost");
    var itemCostInput = $(document.createElement("input"))
      .addClass("item-cost-value")
      .addClass("form-control")
      .attr({
        type: "number",
        name: namePrefix,
        id: description + "-cost",
        value: cost,
      });

    if (showNumber) {
      var cost = +$("#item-cost").text();
      if (
        document.getElementById("free-" + description.replace(/ /gi, "")) !=
        null
      ) {
        cost = 0;
      }
      itemNumberInput.attr("value", "");
      itemCostInput.attr("value", cost);
      itemCostInput.attr("min", 0);
    } else {
      itemNumberInput.attr("value", "N/A");
      itemNumber.hide();
      itemCostInput.attr("min", -1);
      itemCostInput.attr("value", "-1");
      itemCost.hide();
    }

    itemNumber.append(itemNumberInput);
    row.append(itemNumber);
    itemCost.append(itemCostInput);
    row.append(itemCost);

    var itemEntry = $(document.createElement("td")).addClass("item-entry");
    itemEntry.append(
      $(document.createElement("a"))
        .attr({ href: "#" })
        .append(
          $(document.createElement("i"))
            .addClass("fas")
            .addClass("fa-trash")
            .addClass("item-remove")
        )
    );
    row.append(itemEntry);
    $("#equipment > tbody:last-child").append(row);
    $("#submit-btn").show();
    $(".item-cost-value").on("input", setTotalCost);
    setTotalCost();
    if (!showNumber) {
      $("#" + description + "-dropdown").hide();
    }
    addItemRemoveListener();
  });
});
