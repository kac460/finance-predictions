import matplotlib.pyplot as plt
from categories import CATEGORIES
from process_transactions import (
    get_transaction_filenames, 
    category_expenses_for_file,
    total_expenses_in_file,
    TRANSACTIONS_FILE_SUFFIX
)
from os import path
from datetime import date, datetime, timedelta

_MONTH_YEAR_FORMAT = '%B %Y'

def main():
    tomorrow = date.today() + timedelta(days=1)
    dates: list[datetime] = []
    total_monthly_expenses = []
    category_monthly_expenses = {
        category: []
        for category in CATEGORIES
    }
    for filename in get_transaction_filenames(tomorrow.year, tomorrow.month):
        month_year = path.split(filename)[1].replace(TRANSACTIONS_FILE_SUFFIX, '')
        file_date = datetime.strptime(month_year, _MONTH_YEAR_FORMAT)
        dates.append(file_date)
        total_monthly_expenses.append(total_expenses_in_file(filename))
        category_expenses = category_expenses_for_file(filename)
        for category in CATEGORIES:
            category_monthly_expenses[category].append(
                max(category_expenses.get(category, 0), 0)
            )
    categories_sorted = sorted(
        CATEGORIES, 
        key=lambda cat: sum(category_monthly_expenses[cat]),
        reverse=True
    )
    # BY CATEGORY
    plt.figure('Monthly By Category')
    for category in categories_sorted:
        plt.plot(
            dates, 
            category_monthly_expenses[category], 
            label=category
        )
    plt.title('Category Monthly Expenses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Expense ($)')
    plt.legend()
    date_ticks = dates[::1]
    plt.xticks(
        date_ticks, 
        [dt.strftime('%m-%Y') for dt in date_ticks],
        rotation=45
    )

    # TOTAL
    plt.figure('Monthly Total')
    plt.plot(dates, total_monthly_expenses)
    plt.title('Total Monthly Expenses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Monthly Expense ($)')
    plt.xticks(
        date_ticks, 
        [dt.strftime('%m-%Y') for dt in date_ticks],
        rotation=45
    )
    plt.yticks([n*500 for n in range(4, 16)])
    plt.show()


if __name__ == '__main__':
    main()
