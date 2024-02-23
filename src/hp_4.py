# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    return [datetime.strptime(date, "%Y-%m-%d").strftime('%d %b %Y') for date in old_dates]


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()
    dts = []
    _format = datetime.strptime(start, '%Y-%m-%d')
    for a in range(n):
        dts.append(_format + timedelta(days=a))
    return dts


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    daily_date_range = list(zip(date_range(start_date, len(values)), values))
    return daily_date_range


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    columns = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".split(','))
    late_fees = defaultdict(float)
    with open(infile, 'r') as f:
        lines = DictReader(f, fieldnames=columns)
        logs = [row for row in lines]
    logs.pop(0)

    for log in logs:
        patronID = log['patron_id']
        date_due = datetime.strptime(log['date_due'], "%m/%d/%Y")
        date_returned = datetime.strptime(log['date_returned'], "%m/%d/%Y")
        days_late = (date_returned - date_due).days
        late_fees[patronID]+= 0.25 * days_late if days_late > 0 else 0.0
    
    output_fees_data = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in late_fees.items()
    ]
    with open(outfile, 'w') as fle:
        
        wt = DictWriter(fle,['patron_id', 'late_fees'])
        wt.writeheader()
        wt.writerows(output_fees_data)



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
