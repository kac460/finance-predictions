# finance-predictions

A tool for predicting expenses for the next month (with some simple averaging/weighting strategies--nothing fancy--sorry, ML fans!), with additional scripting for visualizing your expenses over time.

## Instructions

### Computing predictions
1. Create a copy of the [Monthly Transactions Google Sheet](https://docs.google.com/spreadsheets/d/1tAU0B2JERHkkEBV7TIup-qKHJk2BSqA6kzL4jzG2Mac/edit?usp=sharing), rename it to `<MonthName> <YYYY>`
2. Enter your expenses for the month in the Expenses section of the `Transactions` sheet.
3. Download the `Transactions` sheet as a CSV file (click `File` -> `Download`) and place the file inside the `transactions/` dir of your local copy of this repo. Note the file should be named `<MonthName> <YYYY> - Transactions.csv`. 
4. Update [hardcoded_predictions.py](./hardcoded_predictions.py) with your own hardcoded predictions as desired.
5. Update [categories.py](./categories.py) to match the categories (including the exact order!) shown on your Google Sheet's `Summary` sheet.
6. Run `python3 calculate_predictions.py`
7. The script will use all the `<MonthName> <YYYY> - Transactions.csv` files in your `transactions/` dir as well as `hardcoded_predictions.py` to predict expenses for each category (printed to standard output)
9. For your next month, create a copy of the sheet you made in the previous instructions, clearing the transactions your reorded under the `Transactions` sheet.
10. Copy/paste the `COPY/PASTE-ABLE PREDICTIONS` into your next month's transactions Google Sheet in the `Summary` sheet's `Expenses` section

### Improving the predictions

After at least 1 month of using this tool, you can try different weighting functions in `weights_functions.py` to see which function would've done the best at predicting your past expenses. 

Run `python3 predictions_tester.py` to see which of the weighting functions has the best historical performance for your expenses. The default used in `calculate_predictions.py` is (because it was best at predicting my own predictions) but you can change it by changing `DEFAULT_WEIGHTING_FUNCTION` in [calculate_predictions.py](./calculate_predictions.py). 


### Visualizing expenses over time

While the main purposes of this repo is to host code for predicting monthly expenses, it also has a script [visualize_expenses_over_time.py](visualize_expenses_over_time.py) for visualizing your monthly total/by category expenses. 

Run `python3 visualize_expenses_over_time.py` and you will get two line charts plotting your monthly total/by category expenses against time. 
- Note the script assumes you have [matplotlib](https://pypi.org/project/matplotlib/) installed (if you do not have it, install it by running `pip install matplotlib`).
- Of course, you need to have at least one (but ideally many more than one) `transactions/` file (as per the instructions in "[Computing predictions](#computing-predictions)") for this script to work.

**Fair warning** - the data viz part of the repo is a bit of a work in progress (I just wanted to get something working asap), and I am not at all familiar with `matplotlib`, so the code and visualizations are a little messy!
