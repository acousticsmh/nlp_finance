import datetime

from sec_edgar_downloader import Downloader


def download_10k(ticker):
    dl = Downloader("company_name", "cn@example.com")
    for year in range(1995, 2024):
        dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")
