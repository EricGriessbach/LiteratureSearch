import csv
import requests

def read_csv(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header row
        return [(row[1], row[5], row[7]) for row in reader]  # Title, PubMed ID, and DOI

def fetch_citations_and_references(doi, pubmed_id):
    if doi:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=citations.externalIds,references.externalIds"
    elif pubmed_id:
        url = f"https://api.semanticscholar.org/graph/v1/paper/PMID:{pubmed_id}?fields=citations.externalIds,references.externalIds"
    else:
        return [], []

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        citations = [(c.get('paperId', ''), c.get('externalIds', {}).get('DOI', '')) for c in data.get('citations', []) if c.get('externalIds')]
        references = [(r.get('paperId', ''), r.get('externalIds', {}).get('DOI', '')) for r in data.get('references', []) if r.get('externalIds')]
        return citations, references
    else:
        print(f"Failed to fetch data for DOI {doi} / PubMed ID {pubmed_id}: ", response.status_code)
        return [], []

    
def main():
    articles = read_csv('database.csv')
    citations_filename = 'citations.csv'
    references_filename = 'references.csv'

    # Initialize the CSV files with headers
    init_csv(citations_filename, ['DOI', 'Citing Paper ID', 'Paper DOI'])
    init_csv(references_filename, ['DOI', 'Cited Paper ID', 'Paper DOI'])

    for Title, DOI, PubMed_ID in articles:
        print(f"Fetching data for {Title}...")
        citations, references = fetch_citations_and_references(DOI, PubMed_ID)
        save_to_csv({DOI or PubMed_ID: citations}, citations_filename, 'Citing Paper ID', mode='a')
        save_to_csv({DOI or PubMed_ID: references}, references_filename, 'Cited Paper ID', mode='a')


def init_csv(filename, headers):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Header row

def save_to_csv(data, filename, header, mode='w'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow(['DOI', header, 'Paper DOI'])  # Header row only for new file
        for doi, papers in data.items():
            for paper_id, paper_doi in papers:
                writer.writerow([doi, paper_id, paper_doi])

if __name__ == "__main__":
    main()

