# pyggy-bank
Excel data entry bot for helping me manage my monthly budget and finances

# Description
pyggy-bank is a simple data entry bot which takes transaction data from a
file and attempts to place it in a 'spending category' based on patterns in the 
transaction narrative / description.<br/>Analysis can then be easily performed on
the previously unorganized data to gain useful insight into one's spending
habits, helping the user cut down on unnecessary spending and maximise on savings.

## Vocabulary
Depending on the user's particular situation, the file 'pyggy-vocab.csv' must be
calibrated accordingly. This file contains the transaction categories on each
row, along with string sequences that match with that category.<br/>

The file format is as follows:<br/>
* type (income or expense?),<br/>
* category name,<br/>
* budget $ for the expense or estimate $ for the income (monthly), and<br/>
* a sequence of upto n ',' separated patterns mapping to this category<br/>

# Usage
First, get your transaction data in a csv file with the following format:<br/>
`Bank Account,Date,Narrative,Debit Amount,Credit Amount,Balance,Categories,Serial`<br/>
However, only Date, Narrative, Debit Amount, and Credit Amount are needed.<br/>
This is the format returned by Westpac, other banks may differ and thus may 
require some tweaking.<br/>

Before running, ensure the following 3 files are present in the directory:<br/>
* `pyggy-vocab.csv`
* `Data.csv`
* `Budget_month_year.xlsx`

Then simply install openpyxl and run the script<br/>

```
pip install openpyxl
python pyggybank.py <month> <year>
```
