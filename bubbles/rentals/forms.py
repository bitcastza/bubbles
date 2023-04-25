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

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.forms import fields, widgets
from django.utils.translation import gettext_lazy as _

from bubbles.inventory import get_item_size_map
from bubbles.inventory.models import Item, Weight
from .models import Rental, RentalItem, RentalPeriod, RequestItem


def get_initial_period():
    date = datetime.date.today()
    period_query_set = RentalPeriod.objects.filter(end_date__gt=date, hidden=False)
    if len(period_query_set) > 0:
        return period_query_set[0]
    return None


class EquipmentTableWidget(widgets.Widget):
    index = {
        "description": 0,
        "size": 1,
        "number": 2,
        "cost": 3,
    }
    template_name = "rentals/widgets/equipment_table_widget.html"

    def __init__(
        self, *args, show_number=False, show_cost=False, item_cost=0, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.item_cost = item_cost
        self.show_number = show_number
        self.show_cost = show_cost

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        item_types = (
            Item.objects.filter(state=Item.AVAILABLE, hidden=False)
            .values("description")
            .distinct()
        )
        free_items = (
            Item.objects.filter(state=Item.AVAILABLE, free=True)
            .values("description")
            .distinct()
        )
        context["widget"]["equipment"] = value
        context["widget"]["item_size_map"] = get_item_size_map()
        context["widget"]["item_types"] = item_types
        context["widget"]["free_items"] = free_items
        context["widget"]["item_cost"] = self.item_cost
        context["widget"]["show_number"] = self.show_number
        context["widget"]["show_cost"] = self.show_cost
        return context

    class Media:
        css = {
            "screen": ("css/equipment_table.css",),
        }
        js = (
            "vendor/gijgo/js/gijgo.min.js",
            "js/equipment_table.js",
        )


class RentalEquipmentTableWidget(EquipmentTableWidget):
    def value_from_datadict(self, data, files, name):
        if name in data:
            # Handle the case where equipment is created from a list of
            # Request/RentalItems
            return data[name]
        result = []
        i = 0
        while True:
            value = data.getlist(f"{name}-{i}")
            i += 1
            if len(value) == 0:
                break
            if len(value) == 1:
                # Equipment item is a single class already
                result.append(value[0])
                continue
            item_dict = {
                "item_description": value[0],
                "item_size": value[1],
                "item_number": value[2],
                "cost": value[3],
            }
            item = Item(
                number=item_dict["item_number"],
                description=item_dict["item_description"],
                hidden=False,
            )
            try:
                rental_item = RentalItem.objects.get(item=item, returned=False)
            except ObjectDoesNotExist:
                rental_item = RentalItem(item=item, cost=int(item_dict["cost"]))
            except RentalItem.MultipleObjectsReturned:
                # Do not crash, just take the first. The view should remove
                # duplicates before creating the form
                rental_item = RentalItem.objects.filter(item=item, returned=False)[0]
            result.append(rental_item)
        return result


class RequestEquipmentTableWidget(EquipmentTableWidget):
    def value_from_datadict(self, data, files, name):
        if name in data:
            # Handle the case where equipment is created from a list of
            # Request/RentalItems
            return data[name]
        result = []
        i = 0
        while True:
            value = data.getlist(f"{name}-{i}")
            i += 1
            if len(value) == 0:
                break
            if len(value) == 1:
                # Equipment item is a single class already
                result.append(value[0])
                continue
            item = {
                "item_description": value[0],
                "item_size": value[1],
            }
            if value[2] != "N/A":
                item["item_number"] = value[2]
            if value[3] != "-1":
                item["cost"] = value[3]
            request_item = RequestItem(**item)
            if request_item not in result:
                result.append(request_item)
        return result


class RequestEquipmentListField(fields.Field):
    widget = RequestEquipmentTableWidget

    def __init__(
        self, *args, show_number=False, show_cost=False, item_cost=0, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.widget.show_number = show_number
        self.widget.show_cost = show_cost
        self.widget.item_cost = item_cost

    def set_show_number(self, value):
        self.widget.show_number = value

    def set_show_cost(self, value):
        self.widget.show_cost = value

    def set_item_cost(self, value):
        self.widget.item_cost = value

    def clean(self, value):
        if value is None:
            return None
        return value


class RentalEquipmentListField(fields.Field):
    widget = RentalEquipmentTableWidget

    def __init__(self, *args, show_cost=False, item_cost=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.show_number = True
        self.widget.show_cost = show_cost
        self.widget.item_cost = item_cost

    def set_show_number(self, value):
        self.widget.show_number = value

    def set_show_cost(self, value):
        self.widget.show_cost = value

    def set_item_cost(self, value):
        self.widget.item_cost = value

    def clean(self, value):
        if value is None:
            return None
        rental_items = []
        errors = []
        for v in value:
            try:
                item = Item.objects.get(
                    number=v.item.number, description=v.item.description, hidden=False
                )
            except ObjectDoesNotExist:
                errors.append(
                    forms.ValidationError(
                        _("%(type)s number %(num)s not found"),
                        code="invalid",
                        params={
                            "type": v.item.description,
                            "num": v.item.number,
                        },
                    )
                )
                continue
            except Item.MultipleObjectsReturned:
                errors.append(
                    forms.ValidationError(
                        _(
                            "There are multiple %(type)s with number %(num)s. Please renumber one before continuing."
                        ),
                        code="invalid",
                        params={
                            "type": v.item.description,
                            "num": v.item.number,
                        },
                    )
                )
                continue
            try:
                rental_item = RentalItem.objects.get(item=item, returned=False)
            except ObjectDoesNotExist:
                rental_item = RentalItem(item=item, cost=int(v.cost))
            except RentalItem.MultipleObjectsReturned:
                # Do not crash, just take the first. The view should remove duplicates
                # before creating the form
                rental_item = RentalItem.objects.filter(item=item, returned=False)[0]
            rental_items.append(rental_item)
        if len(errors) > 0:
            raise forms.ValidationError(errors)
        return rental_items


class EquipmentForm(forms.Form):
    period_state_filter = Rental.REQUESTED
    period = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=widgets.Select(attrs={"class": "form-control"}),
        initial=get_initial_period,
    )
    belt_weight = forms.IntegerField(
        min_value=0,
        max_value=15,
        initial=0,
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, user, rental=None, request_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.rental = rental
        self.request_id = request_id
        if user.has_perm("rental.free_rental"):
            # Free rentals should not select a period
            period_query_set = RentalPeriod.objects.filter(start_date=None)
        else:
            date = datetime.date.today()
            period_query_set = RentalPeriod.objects.filter(
                end_date__gt=date, hidden=False
            )
        self.fields["period"].queryset = period_query_set

    def clean_period(self):
        data = self.cleaned_data["period"]
        if data is None:
            if not self.user.has_perm("rental.free_rental"):
                raise forms.ValidationError(_("This field is required"), code="invalid")

            current_rentals = Rental.objects.filter(user=self.user, state=Rental.RENTED)
            if current_rentals.count() > 0:
                return current_rentals.first().rental_period
            else:
                return RentalPeriod(
                    start_date=datetime.date.today(),
                    default_deposit=0,
                    default_cost_per_item=0,
                    hidden=True,
                )

        existing_periods = Rental.objects.filter(
            user=self.user, rental_period=data, state=self.period_state_filter
        )
        if existing_periods.count() and self.request_id is None:
            raise forms.ValidationError(
                _("You already have a request/rental submitted " "for this period"),
                code="invalid",
            )
        return data

    def clean_belt_weight(self):
        data = self.cleaned_data["belt_weight"]
        if data is None:
            raise forms.ValidationError(_("This field is required"), code="invalid")
        total_weight = Weight.objects.first()
        if total_weight is None and data > 0:
            raise forms.ValidationError(
                _(
                    "No total weight specified by staff, "
                    + "unable to continue. Please send this "
                    + "error to your system administrator."
                ),
                code="invalid",
            )
        return data

    def clean(self):
        super().clean()
        try:
            period = self.cleaned_data["period"]
        except KeyError:
            raise forms.ValidationError(_("Period is required"), code="invalid")

        if self.rental is None:
            state = Rental.REQUESTED
            deposit = period.default_deposit
            self.rental = Rental(
                user=self.user, state=state, deposit=deposit, rental_period=period
            )
        try:
            free_items = (
                Item.objects.filter(state__exact=Item.AVAILABLE, free=True)
                .values("description")
                .distinct()
            )
            free_items = [x["description"] for x in free_items]
            for rental_item in self.cleaned_data["equipment"]:
                rental_item.rental = self.rental
                try:
                    if rental_item.item_description not in free_items:
                        rental_item.cost = (
                            self.rental.rental_period.default_cost_per_item
                        )
                except AttributeError:
                    pass  # Only Request Items have item_description
        except (KeyError, TypeError):
            pass
        return self.cleaned_data


class RequestEquipmentForm(EquipmentForm):
    equipment = RequestEquipmentListField()
    liability = forms.BooleanField(
        label=mark_safe(
            _("I have read and understand the <a href=/docs/terms>terms of rental</a>")
        ),
        widget=widgets.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    period_state_filter = Rental.REQUESTED

    def __init__(self, *args, show_number=False, show_cost=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["equipment"].set_show_number(show_number)
        self.fields["equipment"].set_show_cost(show_cost)


class RentEquipmentForm(EquipmentForm):
    equipment = RentalEquipmentListField(show_cost=True)
    deposit = forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control"})
    )
    period_state_filter = Rental.RENTED

    def __init__(self, *args, rental=None, **kwargs):
        super().__init__(*args, rental=rental, **kwargs)
        if rental:
            self.fields["equipment"].set_item_cost(
                rental.rental_period.default_cost_per_item
            )

    def clean(self):
        super().clean()
        rented_equipment = self.cleaned_data.get("equipment")
        if rented_equipment is None:
            return
        for item in rented_equipment:
            try:
                item = item.item
                if item.state == Item.IN_USE:
                    rental_item = item.rentalitem_set.filter(returned=False).first()
                    if rental_item is None:
                        # Rental item has been returned or state is
                        # incorrect.
                        item.state = Item.AVAILABLE
                        item.save()
                        continue
                    user = rental_item.rental.user
                    user_str = "{first:s} {last:s} ({account:s})".format(
                        first=user.first_name,
                        last=user.last_name,
                        account=user.username,
                    )
                    self.add_error(
                        "equipment",
                        forms.ValidationError(
                            _(
                                "%(type)s number %(num)s not available. It is currently rented to %(user)s"
                            ),
                            code="invalid",
                            params={
                                "type": item.description,
                                "num": item.number,
                                "user": user_str,
                            },
                        ),
                    )

                elif item.state != Item.AVAILABLE:
                    self.add_error(
                        "equipment",
                        forms.ValidationError(
                            _(
                                "%(type)s number %(num)s not available. It is currently %(state)s"
                            ),
                            code="invalid",
                            params={
                                "type": item.description,
                                "num": item.number,
                                "state": item.state[1].lower(),
                            },
                        ),
                    )
            except AttributeError:
                self.add_error(
                    "equipment",
                    forms.ValidationError(
                        _("%(type)s number not valid"),
                        code="invalid",
                        params={
                            "type": item.item_description,
                        },
                    ),
                )


class ReturnEquipmentForm(forms.Form):
    belt_weight = forms.IntegerField(
        min_value=0,
        max_value=15,
        initial=0,
        widget=widgets.NumberInput(attrs={"class": "form-control"}),
    )
    equipment = RentalEquipmentListField()
    deposit = forms.IntegerField(
        widget=widgets.NumberInput(attrs={"class": "form-control", "readonly": True})
    )
    deposit_returned = forms.BooleanField(
        required=False,
        widget=widgets.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, *args, user, rental, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.rental = rental
