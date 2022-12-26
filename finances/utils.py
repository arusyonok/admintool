import typing
from dataclasses import dataclass
from decimal import Decimal

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import OuterRef, Q, QuerySet, Subquery, Sum

from .models import GroupWalletRecord, Balance


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@dataclass
class SubGroupedPeopleAndRecords:
    people: list
    records: QuerySet
    total_amount: Decimal
    wallet_id: int

    @property
    def mean(self) -> Decimal:
        return self.total_amount / len(self.people)

    @property
    def sorted_debt_values(self):
        _max_paid_values = self.records.values("paid_by").annotate(max_paid=Sum("amount"))
        _max_paid_values_dict = {item["paid_by"]: item["max_paid"] for item in _max_paid_values}
        debt_values = []
        for person in self.people:
            if person not in _max_paid_values_dict.keys():
                max_paid = Decimal(0)
            else:
                max_paid = _max_paid_values_dict[person]
            debt_values.append({
                "owner": person,
                "debt": max_paid-self.mean
            })

        return debt_values


def get_sub_grouped_people_and_records_of_wallet(wallet_id: int) -> typing.List[SubGroupedPeopleAndRecords]:
    participating_people_subquery = GroupWalletRecord.objects.filter(
        group_wallet_id=wallet_id, id=OuterRef("pk")
    ).annotate(
        paid_for_people=ArrayAgg('paid_for_users'),
    ).values("paid_for_people")

    sub_grouped_people_records_combo = GroupWalletRecord.objects.annotate(
        paid_for_people=Subquery(participating_people_subquery.values("paid_for_people")),
    ).values(
        "paid_for_people"
    ).annotate(
        paid_by_people=ArrayAgg("paid_by", distinct=True), records=ArrayAgg("id")
    ).values(
        "paid_for_people", "paid_by_people", "records"
    )

    return_dataclass_list = []

    # here basically we check if there are any records at all, by checking inside the query we got from upper code
    if len(sub_grouped_people_records_combo) == 1 and sub_grouped_people_records_combo[0]["paid_for_people"] is None:
        return return_dataclass_list

    sub_grouped_people_records_combo = check_edge_cases(list(sub_grouped_people_records_combo))

    for combo in sub_grouped_people_records_combo:
        records = GroupWalletRecord.objects.filter(id__in=combo["records"])
        return_dataclass_list.append(
            SubGroupedPeopleAndRecords(
                people=combo["paid_for_people"],
                records=records,
                total_amount=sum(records.values_list("amount", flat=True)),
                wallet_id=wallet_id,
            )
        )
    return return_dataclass_list


def check_edge_cases(sub_grouped_people_records_combo_list:  typing.List[typing.Dict]) -> typing.List[typing.Dict]:
    # a lot of ugly code
    new_values = []
    for tet in sub_grouped_people_records_combo_list:
        # find if there is a case when payer is not in the payee list
        payer_not_a_payee_list = list(set(tet["paid_by_people"]) - set(tet["paid_for_people"]))

        for paid_by in payer_not_a_payee_list:
            # if such payer exists, then we need to fix the placement of the payer+payee combo with records
            wrongly_assigned_records = GroupWalletRecord.objects.filter(
                paid_by=paid_by, id__in=tet["records"]
            ).distinct()
            # fix current item of the combo list
            for record in wrongly_assigned_records:
                tet["records"].remove(record.id)
            tet["paid_by_people"].remove(paid_by)

            # assign new items to an outside list so as to attach to the main list later
            new_values.append(dict(
                paid_for_people=tet["paid_for_people"] + [paid_by],
                new_paid_by=[paid_by],
                missing_records=list(wrongly_assigned_records.values_list("id", flat=True)),
            ))

    for new_value in new_values:
        dict_item = next(
            (
                item for item in sub_grouped_people_records_combo_list
                if set(item["paid_for_people"]) == set(new_value["paid_for_people"])
            ), None
        )
        if dict_item:
            dict_item["records"].extend(new_value["missing_records"])
            dict_item["paid_by_people"].extend(new_value["new_paid_by"])
        else:
            sub_grouped_people_records_combo_list.append(dict(
                paid_for_people=new_value["paid_for_people"],
                paid_by_people=new_value["new_paid_by"],
                records=new_value["missing_records"]
            ))

    final_list = [item for item in sub_grouped_people_records_combo_list if item["records"]]

    return final_list


def calculate_and_set_debt_values(debt_values, wallet_id):
    sorted_debt_values = sorted(debt_values, key=lambda d: d['debt'], reverse=True)

    most_paid = sorted_debt_values[0]
    least_paid = sorted_debt_values[-1]

    # happy days
    loaned_to = least_paid["owner"]
    loaned_from = most_paid["owner"]

    balance_obj, created = Balance.objects.get_or_create(
        loaned_from_id=loaned_from,
        loaned_to_id=loaned_to,
        group_wallet_id=wallet_id
    )

    difference = most_paid["debt"] + least_paid["debt"]   # least ome should always be minus

    if difference < 0:
        balance_obj.amount = most_paid["debt"]
        balance_obj.save()

        sorted_debt_values[-1]["debt"] = difference
        sorted_debt_values.pop(0)
        calculate_and_set_debt_values(sorted_debt_values, wallet_id)
    elif difference > 0:
        balance_obj.amount = abs(least_paid["debt"])
        balance_obj.save()

        sorted_debt_values[0]["debt"] = difference
        sorted_debt_values.pop()
        calculate_and_set_debt_values(sorted_debt_values, wallet_id)
    elif difference == 0:
        balance_obj.amount = abs(least_paid["debt"])
        balance_obj.save()
    else:
        raise ValueError("Something went wrong with balance calculation")


def calculate_balances(wallet_id):
    sub_grouped_people_and_records = get_sub_grouped_people_and_records_of_wallet(wallet_id)

    for data in sub_grouped_people_and_records:
        debt_values = data.sorted_debt_values

        calculate_and_set_debt_values(debt_values, data.wallet_id)


def get_balances(current_user, wallet_id):
    calculate_balances(wallet_id)  # TODO: move this somewhere sensible
    user_balances = Balance.objects.filter(
        Q(loaned_from_id=current_user) | Q(loaned_to_id=current_user),
        group_wallet_id=wallet_id
    )
    balances = []
    for balance in user_balances:
        amount = int(balance.amount)
        balances.append({
            balance.loaned_from.first_name: amount,
            balance.loaned_to.first_name: -amount
        })

    return balances
