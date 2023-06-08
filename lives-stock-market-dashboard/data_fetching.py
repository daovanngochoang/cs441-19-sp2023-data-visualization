
from datetime import datetime, timedelta
from typing import List

import yfinance
import pandas as pd
from pytickersymbols import PyTickerSymbols


stock_data = PyTickerSymbols()

valid_keys = {
    'revenuePerShare',
    'twoHundredDayAverage',
    'sector',
    'recommendationKey',
    'shortRatio',
    'totalRevenue',
    'earningsQuarterlyGrowth',
    'longBusinessSummary',
    'overallRisk',
    'bidSize',
    'regularMarketPreviousClose',
    'bookValue',
    'totalCash',
    'numberOfAnalystOpinions',
    'regularMarketDayLow',
    'profitMargins',
    'industryDisp',
    'maxAge',
    'returnOnAssets',
    'impliedSharesOutstanding',
    'ask',
    'phone',
    'trailingAnnualDividendYield',
    'fiftyTwoWeekLow',
    'firstTradeDateEpochUtc',
    'totalDebt',
    'regularMarketDayHigh',
    'averageVolume',
    'beta',
    'trailingEps',
    'shortPercentOfFloat',
    '52WeekChange',
    'sharesShortPreviousMonthDate',
    'returnOnEquity',
    'nextFiscalYearEnd',
    'totalCashPerShare',
    'enterpriseToEbitda',
    'forwardEps',
    'governanceEpochDate',
    'fullTimeEmployees',
    'mostRecentQuarter',
    'averageDailyVolume10Day',
    'boardRisk',
    'regularMarketVolume',
    'trailingAnnualDividendRate',
    'netIncomeToCommon',
    'pegRatio',
    'fiftyTwoWeekHigh',
    'messageBoardId',
    'lastFiscalYearEnd',
    'debtToEquity',
    'operatingCashflow',
    'currentRatio',
    'volume',
    'payoutRatio',
    'quoteType',
    'financialCurrency',
    'ebitdaMargins',
    'regularMarketOpen',
    'priceToBook',
    'targetLowPrice',
    'trailingPegRatio',
    'state',
    'open',
    'operatingMargins',
    'shortName',
    'quickRatio',
    'compensationRisk',
    'compensationAsOfEpochDate',
    'country',
    'zip',
    'dateShortInterest',
    'sharesPercentSharesOut',
    'priceHint',
    'heldPercentInstitutions',
    'bid',
    'fiftyDayAverage',
    'currency',
    'recommendationMean',
    'currentPrice',
    'grossMargins',
    'enterpriseValue',
    'timeZoneShortName',
    'symbol',
    'targetMedianPrice',
    'heldPercentInsiders',
    'website',
    'underlyingSymbol',
    'sharesShortPriorMonth',
    'enterpriseToRevenue',
    'targetMeanPrice',
    'longName',
    'targetHighPrice',
    'freeCashflow',
    'address1',
    'sharesOutstanding',
    'forwardPE',
    'timeZoneFullName',
    'industry',
    'floatShares',
    'revenueGrowth',
    'averageVolume10days',
    'city',
    'ebitda',
    'auditRisk',
    'shareHolderRightsRisk',
    'previousClose',
    'trailingPE',
    'dayHigh',
    'marketCap',
    'exchange',
    'askSize',
    'uuid',
    'SandP52WeekChange',
    'grossProfits',
    'earningsGrowth',
    'sharesShort',
    'priceToSalesTrailing12Months',
    'gmtOffSetMilliseconds',
    'dayLow'
}

class DataFetching:
    def __init__(self) -> None:
        symbols = ['AMZN','GOOG','MSFT','META', 'AAPL']+[data["symbol"] for data in stock_data.get_all_stocks()]
        
        self.symbols: list = filter(lambda item: item is not None, symbols)
        self.default: list = ['AMZN','GOOG','MSFT','META', 'AAPL']
    
    def fetch_data(self, start_date, end_date, company_symbols=None):
        if company_symbols in [None, []]:
            company_symbols = self.default
        
        if len(company_symbols) > 1:
        
            tickers = yfinance.Tickers(company_symbols)
        
        elif len(company_symbols) == 1:
            tickers = yfinance.Ticker(company_symbols[0])
            

        tickers_hist = tickers.history(start=start_date, end=end_date)

        return tickers_hist

    def fetch_info(self, symbol):
        data =  yfinance.Ticker(symbol).info
        return {key: data[key] for key in data if key in valid_keys}   
    
    def fetch_close_price(self, start_date, end_date, company_symbols=None):
        print(start_date, end_date, company_symbols)
        data = self.fetch_data(start_date, end_date, company_symbols)
        return data["Close"].reset_index()
    
    def fetch_devidends(self, start_date, end_date, company_symbols=None):
        data = self.fetch_data(start_date, end_date, company_symbols)
        return data["Devidends"].reset_index()
    
    def fetch_high_price(self, start_date, end_date, company_symbols=None):
        data = self.fetch_data(start_date, end_date, company_symbols)
        return data["High"].reset_index()
    
    def fetch_low_price(self, start_date, end_date, company_symbols=None):
        data = self.fetch_data(start_date, end_date, company_symbols)
        return data["Low"].reset_index()
    
    def fetch_open_price(self, start_date, end_date, company_symbols=None):
        data = self.fetch_data(start_date, end_date, company_symbols)
        return data["Open"].reset_index()
    
    def fetch_volume(self, start_date, end_date, company_symbols=None):
        data = self.fetch_data(start_date, end_date, company_symbols)
        return data["Volume"].reset_index()
    
    def fetch_stock_splits(self, start_date, end_date, company_symbols=None):
        data = self.fetch_data(start_date, end_date, company_symbols)
        return data["Stock Splits"].reset_index()
    
    
    
    
data_fetching = DataFetching()