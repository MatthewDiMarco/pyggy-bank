import bookkeeper as bk
import sys

def main():
     
    # validate imports
    if len(sys.argv) is not 3:
        print('SYNTAX: python pyggybank.py <month> <year>')
        print('e.g. ... july 2020')
        sys.exit(0)
    
    # important files that should be in the directory
    FL_DATA = 'Data.csv'
    FL_BOOK = 'Budget_{}_{}.xlsx'.format(sys.argv[1].upper(), sys.argv[2]) # month, yr
    FL_VOCAB = 'pyggy-vocab.csv'
     
    # init bot   
    booker = bk.Bookkeeper()
    booker.build_vocab(FL_VOCAB)
    booker.open(FL_BOOK)
    
    # get transactions
    try:
        transactions = get_transactions(FL_DATA)
    except IOError as e:
        print('Error: {}'.format(str(e)))
        sys.exit(0)
    
    # process transactions
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
                booker.insert(d[1], debit, credit, booker.categorize(tran))
        except bk.BookkeeperError as e:
            uncategorized_trans.append(tran)
            
    # output results
    print('\n{} transaction successfully categorized and booked!'.format(
        len(transactions) - len(uncategorized_trans)
    ))
    print('{} unknown transactions:'.format(
        len(uncategorized_trans)
    ))
    print('===================================================')
    for ii,tran in enumerate(uncategorized_trans):
        details = tran.split(',')
        debit,credit = 0,0
        try: debit = float(details[3])
        except ValueError as e: pass
        try: credit = float(details[4])
        except ValueError as e: pass
        amount = '-{}'.format(debit) if debit > credit else '+{}'.format(credit)
        desc = [d for d in details[2].split(' ') if d != '']
        new_desc = []
        for ii in range(len(desc)): 
            new_desc.append(desc[ii])
            new_desc.append(' ')
        desc = ''.join(new_desc)
        print('{}. {}   {}'.format(
            ii+1, desc, amount
        ))
    
    # user option: 'other' category or dump to file?
    print('\nWhat would you like to do with these transactions?')
    print('1) Add to \'Other\' Category   2) Dump to file   3) Discard')
    
    op = -1
    while op not in range(1, 4):
        try:
            op = int(input())
        except ValueError:
            print('try an integer')
            
        if op == 1:
            for tran in uncategorized_trans:
                try:
                    if tran != '' and tran != None:
                        d = tran.split(',')
                        debit,credit = 0,0
                        try: debit = float(d[3])
                        except ValueError as e: pass
                        try: credit = float(d[4])
                        except ValueError as e: pass
                        if debit > credit: typ = 'EXP'
                        else: typ = 'INC'
                        booker.insert(d[1], debit, credit, (typ, 'Other', 50))
                except bk.BookkeeperError as e:
                    print(str(e))
        elif op == 2:
            try:
                save = open('unknown-transactions.csv', 'w')
                for tran in uncategorized_trans: 
                    save.write(tran)
                    save.write('\n')
                save.close()
            except IOError as e:
                print(str(e))
        elif op == 3:
            pass # discard
    
    # save and close excel sheet        
    booker.close()

def get_transactions(filename):
    try:
        fl = open(filename)
        data = fl.read()
        fl.close()
    except IOError:
        raise IOError('Provided file is invalid')
    
    trans = data.split('\n')
    trans = [tran for tran in trans if 'tfr westpac' not in tran.split(',')[2].lower()]
    return trans[1:] # skip header row

if __name__ == '__main__':
    main()