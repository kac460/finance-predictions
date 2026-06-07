from datetime import date
from weights_functions import (
    exponential_weights,
    even_weights,
    even_weights_last_year_only,
    incrementing_weights,
)
from hardcoded_predictions import HARDCODED_PREDICTIONS
from process_transactions import (
    category_expenses_for_month,
    START_YEAR,
    START_MONTH_NUM,
)
from pprint import pprint


# returns (year, month_num) for (start_year, start_month_num) <= (year, month_num) < (end_year, end_month)}
def months_up_to(
    end_year: int, 
    end_month_num: int, 
    start_year: int = START_YEAR, 
    start_month_num: int = START_MONTH_NUM,
) -> list[tuple[int, int]]:
    year_months: list[tuple[int, int]] = []
    for year in range(start_year, end_year + 1):
        for month_num in range(1, 13):
            if month_num < start_month_num and year == start_year:
                continue
            elif month_num == end_month_num and year == end_year:
                break
            else:
                year_months.append((year, month_num))
    return year_months


# returns {(year, month_num): compute_predictions(year, month_num) | (START_YEAR, START_MONTH_NUM) <= (year, month_num) < today }
def predictions_for_every_month(weights_function):
    from calculate_predictions import compute_predictions

    today = date.today()
    months_up_to_today = months_up_to(today.year, today.month)
    all_predictions = {
        year_month: compute_predictions(*year_month, weights_function)
        for year_month in months_up_to_today
    }
    return all_predictions


def expenses_for_every_month():
    today = date.today()
    months_up_to_today = months_up_to(today.year, today.month)
    print(f'months_up_to_today: {months_up_to_today}')
    all_expenses = {
        year_month: category_expenses_for_month(*year_month)
        for year_month in months_up_to_today
    }
    return all_expenses


def month_expenses_predictions_diff(
    month_expenses, month_predictions, ignore_hardcoded=True
):
    diffs = {}
    for category in month_predictions:
        # HARDCODED_PREDICTIONS have changed over the years (e.g. rent increased)
        # So the old predictions are likely to be dispraportionately bad
        # Which would bias the comparisons (given some weights_functions assign steeper discounts to older months)
        # So we ignore hardcoded predictions by default
        if ignore_hardcoded and category in HARDCODED_PREDICTIONS:
            continue
        expense = month_expenses.get(category, 0)
        prediction = month_predictions[category]
        diff = abs(expense - prediction)
        print(
            f"{category} - EXPENSE: {expense}, PREDICTION: {prediction}, DIFF: {diff}"
        )
        diffs[category] = diff
    return diffs


def all_expenses_predictions_diff(weights_function, all_expenses):
    all_predictions = predictions_for_every_month(weights_function)
    all_diffs = {}
    for year_month in all_expenses:
        month_predictions = all_predictions[year_month]
        if month_predictions is None:
            continue
        month_expenses = all_expenses[year_month]
        month_diff = month_expenses_predictions_diff(month_expenses, month_predictions)
        all_diffs[year_month] = month_diff
    print(f"ALL DIFFS for {weights_function.__name__}:")
    pprint(all_diffs)
    return all_diffs


_PLACEHOLDER_MONTH_YEAR = (2026, 4)


def avg_category_diffs(
    weights_function, all_expenses, first_year=START_YEAR, first_month=START_MONTH_NUM
):
    today = date.today()
    year_months = months_up_to(today.year, today.month, first_year, first_month)
    monthly_diffs = all_expenses_predictions_diff(weights_function, all_expenses)
    # for any y,m: monthly_diffs[(y,m)] has all the categories
    # so this is a hacky way of getting all the categories
    categories = monthly_diffs[_PLACEHOLDER_MONTH_YEAR].keys()
    num_months = len(monthly_diffs)
    avg_diffs = {
        category: sum(
            [
                monthly_diffs[year_month][category]
                for year_month in year_months
                if year_month in monthly_diffs
            ]
        )
        / num_months
        for category in categories
    }
    return avg_diffs


def best_weights_function():
    all_expenses = expenses_for_every_month()
    weights_functions_to_test = [
        exponential_weights,
        even_weights,
        even_weights_last_year_only,
        incrementing_weights,
    ]
    weights_functions_avg_category_diffs = {}
    weights_functions_avg_category_diffs_last_12m = {}
    last_year = date.today().year - 1
    curr_month = date.today().month
    for weights_function in weights_functions_to_test:
        weights_functions_avg_category_diffs[weights_function] = avg_category_diffs(
            weights_function, all_expenses
        )
        weights_functions_avg_category_diffs_last_12m[weights_function] = (
            avg_category_diffs(weights_function, all_expenses, last_year, 1)
        )
    print("---------\n\n\n\n")
    print("AVG CATEGORY DIFFS ALL TIME:")
    pprint(weights_functions_avg_category_diffs)
    print(f"AVG CATEGORY DIFFS since {curr_month}/{last_year}:")
    pprint(weights_functions_avg_category_diffs_last_12m)
    print("AVG TOTAL DIFFS ALL TIME:")
    print_total_diffs = lambda diffs: pprint(
        {func_name: sum(diffs[func_name].values()) for func_name in diffs}
    )
    print_total_diffs(weights_functions_avg_category_diffs)
    print(f"AVG TOTAL DIFFS since {curr_month}/{last_year}::")
    print_total_diffs(weights_functions_avg_category_diffs_last_12m)
    return min(
        weights_functions_avg_category_diffs_last_12m,
        key=lambda func: sum(
            weights_functions_avg_category_diffs_last_12m[func].values()
        ),
    )


def main():
    print(f"best: {best_weights_function()}")


if __name__ == "__main__":
    main()
