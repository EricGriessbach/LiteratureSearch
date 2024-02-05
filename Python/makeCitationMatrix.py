import csv
import pandas as pd
import numpy as np

def read_csv_to_dict(filename, key_col, value_col):
    data = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header row
        for row in reader:
            key = row[key_col - 1]  # Adjust for 0-based indexing
            value = row[value_col - 1]  # Adjust for 0-based indexing
            if key in data:
                data[key].append(value)
            else:
                data[key] = [value]
    return data

def read_doi_pubmed_to_title(filename):
    data = {}
    date_data = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header row
        for row in reader:
            doi = row[5]  # DOI in column 6 (0-based index 5)
            pubmed_id = row[7]  # PubMed ID in column 8 (0-based index 7)
            title = row[1]  # Title in column 2 (0-based index 1)
            date = row[3]  
            identifier = doi if doi else pubmed_id
            data[identifier] = title
            date_data[identifier] = date
    return data, date_data


def create_citation_matrix(citations, references, doi_pubmed_to_title, date):
    all_dois = set(citations.keys()).union(set(references.keys()))
    all_titles = {doi: doi_pubmed_to_title.get(doi, doi) for doi in all_dois}
    all_dates = {doi: date.get(doi, "Unknown Date") for doi in all_dois}  # Default to "Unknown Date" if not found
    doi_to_index = {doi: idx for idx, doi in enumerate(all_titles.keys())}  # Map DOIs to indices
    citation_matrix = pd.DataFrame(0, index=all_titles.values(), columns=all_titles.values())
    
    # Initialize an empty set for edges to ensure uniqueness
    edges = set()

    # Populate citation matrix and collect edges for citations
    for cited_doi, citing_dois in citations.items():
        cited_index = doi_to_index.get(cited_doi)
        if cited_index is not None:  # Ensure cited DOI is in the matrix
            for citing_doi in citing_dois:
                citing_index = doi_to_index.get(citing_doi)
                if citing_index is not None:  # Ensure cited DOI is in the matrix
                    citation_matrix.iat[citing_index, cited_index] = 1
                    edges.add((citing_index, cited_index))  # Add edge with correct direction

    # Collect edges for references, ensuring they are unique and correctly directed
    for citing_doi, cited_dois in references.items():
        citing_index = doi_to_index.get(citing_doi)
        if citing_index is not None:  # Ensure cited DOI is in the matrix
            for cited_doi in cited_dois:
                cited_index = doi_to_index.get(cited_doi)
                if cited_index is not None:  # Ensure citing DOI is in the matrix
                    citation_matrix.iat[citing_index, cited_index] = 1
                    edges.add((citing_index, cited_index))  

    citation_count = citation_matrix.sum(axis=0)
    
    # Print the 10 most cited papers
    print(citation_count.nlargest(10))
    
    title_date_df = pd.DataFrame({
        'Id': range(len(all_titles)),
        'Label': list(all_titles.values()),
        'Date': [pd.to_datetime(all_dates[doi]).year if pd.to_datetime(all_dates[doi], errors='coerce') is not pd.NaT else "Unknown" for doi in all_dois],
        'CitationCount': citation_count
    })

    # Convert unique edges set to DataFrame
    edge_df = pd.DataFrame(list(edges), columns=['Source', 'Target'])

    return citation_matrix, title_date_df, edge_df




def main():
    # Load DOI/PubMed ID to title mapping
    doi_pubmed_to_title, date = read_doi_pubmed_to_title('database.csv')
    # Load citation and reference data
    citations = read_csv_to_dict('citations.csv', 1, 3)
    references = read_csv_to_dict('references.csv', 1, 3)

    # Create citation matrix and title-date DataFrame
    citation_matrix, title_date_df, edge_df = create_citation_matrix(citations, references, doi_pubmed_to_title, date)

    # Save the citation matrix to a CSV file
    citation_matrix.to_csv('citation_matrix.csv', sep='|', encoding='utf-8')

    # Save the title-date DataFrame to a CSV file
    title_date_df.to_csv('node_attributes.csv', sep=',', index=False, encoding='utf-8')
    edge_df.to_csv('edge_attributes.csv', index=False, encoding='utf-8')


if __name__ == "__main__":
    main()
