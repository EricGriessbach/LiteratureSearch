import os
import csv
import requests


def fetch_motor_learning_literature(api_key, output_file, start_year, end_year, start_index=0):
    url = "https://api.elsevier.com/content/search/scopus"
    query = f"TITLE-ABS-KEY({{implicit motor learning}} OR {{explicit motor learning}}) AND PUBYEAR AFT {start_year-1} AND PUBYEAR BEF {end_year+1}"
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json"
    }
    print(query)
    fetched_articles = 0
    total_articles = None

    while total_articles is None or fetched_articles < total_articles:
        params = {
            "query": query,
            #"field": "eid,title,author,coverDate,sourceTitle,doi,citedby-count,pubmed_id",
            "count": 200,
            "sort": "relevance",
            "start": start_index
        } 
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            total_articles = int(data.get('search-results', {}).get('opensearch:totalResults', 0))
            entries = data.get('search-results', {}).get('entry', [])

            # Determine if the file already exists to decide whether to write headers
            file_exists = os.path.isfile(output_file)

            with open(output_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["EID", "Title", "Authors", "Cover Date", "Source Title", "DOI", "Cited By Count", "PubMed ID"])
                for item in entries:
                    writer.writerow([
                        item.get('eid', ''),
                        item.get('dc:title', ''),
                        '; '.join([author.get('authname', '') for author in item.get('author', [])]),
                        item.get('prism:coverDate', ''),
                        item.get('prism:sourceTitle', ''),
                        item.get('prism:doi', ''),
                        item.get('citedby-count', ''),
                        item.get('pubmed-id', '')
                    ])

            fetched_articles += len(entries)
            print(f"Fetched {len(entries)} articles, total fetched: {fetched_articles}/{total_articles}")
            start_index += 200
        else:
            print("Failed to fetch data: ", response.status_code)
            break

# Usage
api_key = '' # insert you SCOPUS API Key here, e.g., 'xxxxxxxxxxxxxxx' or os.getenv('SCOPUS_API_KEY')
output_file = "database.csv"

date_ranges = [
    (1860, 1980),  # Covers 1860 to 1999
    (1981, 1999),  # Covers 1860 to 1999
    (2000, 2003),  # Covers 2000 to 2004
    (2004, 2006),  # Covers 2000 to 2004
    (2007, 2009),  # Covers 2005 to 2009
   (2010, 2013),  # Covers 2010 to 2014
    (2014, 2016),  # Covers 2015 to 2018
    (2017, 2019),  # Covers 2019 to 2023
    (2020, 2021),   # Covers only the year 2024
    (2022, 2023),   # Covers only the year 2024
    (2024, 2025),   # Covers only the year 2024

]

for start_year, end_year in date_ranges:
    fetch_motor_learning_literature(api_key, output_file, start_year, end_year)

