# pyggy-bank
Excel data entry bot for helping me manage my monthly budget and finances

# Description
pyggy-bank is a simple data entry bot which takes transaction data from a csv
file and attempts to place it in a 'spending category' based on keywords in the 
transaction narrative / description.<br/>

# Vocabulary
Depending on the user's particular situation, the file 'pyggy-vocab.csv' must be
calibrated accordingly. This file contains the transaction categories on each
row, along with keywords that match with that category. The file format is as
follows:<br/>
type (income or expense?)<br/>
category name<br/>
budget $ for the expense or estimate $ for the income (monthly), and<br/>
a sequence of upto n ',' separated patterns mapping to this category<br/>

# Usage
First, get your transaction data in a csv file with the following format:<br/>
Bank Account,Date,Narrative,Debit Amount,Credit Amount,Balance,Categories,Serial<br/>
However, only Date, Narrative, Debit Amount, and Credit Amount are needed. This 
is the format returned by Westpac, other instutions may differ and thus may 
require some tweaking.<br/>

Before running, ensure the following 3 files are present in the directory:<br/>
pyggy-vocab.csv, Data.csv, Budget_<month>_<year>.xlsx

```
pip install openpyxl
python pyggybank.py <month> <year>
```