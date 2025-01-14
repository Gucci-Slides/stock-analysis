# services/data_collector/src/utils/sp500.py
import pandas as pd

def get_sp500_symbols():
    """Get list of S&P 500 symbols using Wikipedia"""
    try:
        # Read S&P 500 table from Wikipedia
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tables = pd.read_html(url)
        sp500_table = tables[0]
        symbols = sp500_table['Symbol'].tolist()
        return symbols
    except Exception as e:
        print(f"Error fetching S&P 500 symbols: {str(e)}")
        return []