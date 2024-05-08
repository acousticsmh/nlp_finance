from sec_edgar_downloader import Downloader

# Initialize a downloader instance.
dl = Downloader("MyCompanyName", "my.email@domain.com")

# Define the companies and the range of years
companies = ["AAPL", "MSFT", "GOOGL"]
start_year = 1995
end_year = 1996

# Download 10-K filings for each company
for company in companies:
    for year in range(start_year, end_year + 1):
        dl.get("10-K", company, after=f"{year}-01-01", before=f"{year}-12-31")

print("Download complete.")
