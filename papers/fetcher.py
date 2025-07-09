# papers/fetcher.py

from typing import List, Dict, Optional
import requests
import csv
import xml.etree.ElementTree as ET

# --- Constants ---
BASE_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
BASE_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# --- Step 1: Get paper IDs ---
def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(BASE_ESEARCH_URL, params=params)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]

# --- Step 2: Fetch full paper details using EFetch (XML format) ---
def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    ids_str = ",".join(pubmed_ids)
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml"
    }
    response = requests.get(BASE_EFETCH_URL, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        authors = []
        companies = []
        email = None

        for author in article.findall(".//Author"):
            affiliation = author.findtext("AffiliationInfo/Affiliation") or ""
            name_parts = [
                author.findtext("ForeName") or "",
                author.findtext("LastName") or "",
            ]
            full_name = " ".join(name_parts).strip()

            if is_non_academic_affiliation(affiliation):
                authors.append(full_name)
                companies.append(affiliation)

            if not email and "@" in affiliation:
                email = extract_email(affiliation)

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(authors),
            "Company Affiliation(s)": "; ".join(companies),
            "Corresponding Author Email": email or "N/A"
        })

    return papers

# --- Step 3: Heuristics to detect non-academic affiliations ---
def is_non_academic_affiliation(affiliation: str) -> bool:
    affiliation_lower = affiliation.lower()
    academic_keywords = ["university", "institute", "college", "hospital", "school"]
    company_keywords = ["inc", "ltd", "pharma", "biotech", "therapeutics", "labs", "genomics"]

    return (
        any(word in affiliation_lower for word in company_keywords) and
        not any(word in affiliation_lower for word in academic_keywords)
    )

def extract_email(text: str) -> Optional[str]:
    import re
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0) if match else None

# --- Step 4: Save to CSV ---
def save_to_csv(data: List[Dict], filename: str):
    if not data:
        print("No data to write.")
        return
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# --- Step 5: Main function called from CLI ---
def fetch_and_process_papers(query: str, output_file: Optional[str], debug: bool = False):
    if debug:
        print(f"Fetching PubMed IDs for query: {query}")
    pubmed_ids = fetch_pubmed_ids(query)

    if debug:
        print(f"Found {len(pubmed_ids)} papers. Fetching full details...")

    papers = fetch_paper_details(pubmed_ids)

    if output_file:
        save_to_csv(papers, output_file)
        print(f"Saved {len(papers)} records to {output_file}")
    else:
        for paper in papers:
            print("-" * 40)
            for key, value in paper.items():
                print(f"{key}: {value}")
