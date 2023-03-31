from datetime import date
from hardcoded_predictions import HARDCODED_PREDICTIONS
from weights_functions import incrementing_weights, weighted_avg
from process_transactions import (
    get_transaction_filenames,
    total_expenses_in_file,
    category_expenses_for_file
)
from categories import CATEGORIES


_DEFAULT_WEIGHTING_FUNCTION = incrementing_weights

def print_average_expenses(year, month_num):
    filenames = get_transaction_filenames(year, month_num)
    print("-----------\n")
    print(f'AVERAGE MONTHLY EXPENSE: {sum([total_expenses_in_file(filename) for filename in filenames])/len(filenames)}')
    print("-----------\n")


'''
Returns a dictionary in the form
{ category (string): prediction (float) }
'''
def compute_predictions(year, month_num, weights_function=_DEFAULT_WEIGHTING_FUNCTION):
    filenames = get_transaction_filenames(year, month_num)
    if len(filenames) == 0:
        print(f'NO FILES PRE-{month_num}/{year}')
        return None
    category_expenses_for_files = [category_expenses_for_file(filename) for filename in filenames]
    predictions = {}
    # we assume all categories are present in the first category_expenses dict
    for category in category_expenses_for_files[0]:
        category_expenses = [category_expense.get(category, 0) for category_expense in category_expenses_for_files]
        predictions[category] = HARDCODED_PREDICTIONS.get(category, weighted_avg(
            category_expenses,
            weights_function(len(category_expenses))
        ))
    return predictions


def main():
    today = date.today()
    final_predictions = compute_predictions(today.year, today.month)
    print_average_expenses(today.year, today.month)

    print("RAW:")
    print(final_predictions)
    print("-----------")
    print('COPY/PASTE-ABLE PREDICTIONS')
    for category in CATEGORIES:
        print(final_predictions.get(category))


if __name__ == '__main__':
    main()
