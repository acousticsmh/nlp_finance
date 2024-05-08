import os

from bs4 import BeautifulSoup


def load_and_clean_html_texts(company_ticker):
    filings_directory = os.path.join(
        os.getcwd(), "sec-edgar-filings", company_ticker, "10-K"
    )

    clean_texts = []

    for root, _, files in os.walk(filings_directory):
        for file in files:
            if file.endswith(".txt"):
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as file_content:
                        soup = BeautifulSoup(file_content, "html.parser")
                        text = soup.get_text(separator=" ", strip=True)
                        clean_texts.append(text)
                except:
                    print("Issue with " + root)

    return clean_texts
