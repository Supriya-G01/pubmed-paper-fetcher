import argparse
from papers.fetcher import fetch_and_process_papers

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors")
    parser.add_argument("query", help="PubMed query string")
    parser.add_argument("-f", "--file", help="CSV file to save results")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    fetch_and_process_papers(query=args.query, output_file=args.file, debug=args.debug)

if __name__ == "__main__":
    main()
