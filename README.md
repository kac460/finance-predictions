# finance-predictions

A tool for predicting expenses for the next month.

## Instructions

### Computing predictions
1. Create a copy of the [Monthly Transactions Google Sheet](https://docs.google.com/spreadsheets/d/1tAU0B2JERHkkEBV7TIup-qKHJk2BSqA6kzL4jzG2Mac/edit?usp=sharing), rename it to `<MonthName> <YYYY>`
2. Enter your expenses for the month in the Expenses section of the `Transactions` sheet.
3. Download the `Transactions` sheet as a CSV file (click `File` -> `Download`) and place the file at the top-level of your local copy of this repo. Note the file should be named `<MonthName> <YYYY> - Transactions.csv`. 
4. Update the [hardcoded_predictions.py](./hardcoded_predictions.py) with your own hardcoded predictions as desired.
5. Run `python3 calculate_predictions.py`
6. The script will use all the `<MonthName> <YYYY> - Transactions.csv` as well as `hardcoded_predictions.py` to predict expenses for each category (printed to standard output)
7. Copy/paste the `COPY/PASTE-ABLE PREDICTIONS` into your next month's transactions Google Sheet in the `Summary` sheet's `Expenses` section

### Improving the predictions

After at least 1 month of using this tool, you can try different weighting functions in `weights_functions.py` to see which function would've done the best at predicting your past expenses. 

Run `python3 predictions_tester.py` to see which of the weighting functions has the best historical performance for your expenses. The default used in `calculate_predictions.py` is (because it was best at predicting my own predictions) but you can change it by changing `DEFAULT_WEIGHTING_FUNCTION` in [calculate_predictions.py](./calculate_predictions.py). 
