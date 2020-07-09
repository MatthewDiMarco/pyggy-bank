import bookkeeper as bk

def main():
    try:
        transactions = read_file('data_example.csv')[1:]
        #filter transactions
        #remove simple transfers in which money is being moved around accounts (not actual income/expense)
        transactions = [tran for tran in transactions if 'tfr westpac' not in tran.split(',')[2].lower()]
    except IOError as e:
        print('Error: {}'.format(str(e)))
        
    booker = init_bookkeeper()
    uncategorized_trans = []
    for tran in transactions:
        try:
            if tran != '' and tran != None:
                d = tran.split(',')
                debit,credit = 0,0
                try: debit = float(d[3])
                except ValueError as e: pass
                try: credit = float(d[4])
                except ValueError as e: pass
                booker.insert(debit, credit, booker.categorize(tran))
        except bk.BookkeeperError as e:
            uncategorized_trans.append(tran)
    print('Failed to Categorize {}/{} Transactions'.format(
        len(uncategorized_trans), len(transactions)
    ))
    for tran in uncategorized_trans:
        details = tran.split(',')
        print(details[2])
            
        booker.close()

def init_bookkeeper():
    vocab_lines = read_file('vocabulary_example.csv')[1:]
    booker = bk.Bookkeeper()
    booker.build_vocab(vocab_lines)
    booker.open('budget_template.xlsx')
    return booker

def read_file(filename):
    try:
        fl = open(filename)
        data = fl.read()
        fl.close()
    except IOError:
        raise IOError('Provided file is invalid')
    return data.split('\n')

if __name__ == '__main__':
    main()