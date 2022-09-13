import pandas as pd
import requests
import argparse

# This script searches HathiTrust for OCLC numbers from a CSV and creates a new CSV with the metadata of any matches.

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Enter filename with csv.')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.csv\'): ')


# From the Hathi API documentation: https://www.hathitrust.org/bib_api

hURL_brief = 'http://catalog.hathitrust.org/api/volumes/brief/oclc/'

# Reads CSV as DataFrame, grabs OCLC identifiers from column named "oclc_id."
df = pd.read_csv(filename)
df.dropna(subset=['oclc_id'], inplace=True)   # Drop blank values.
oclc_identifiers = df['oclc_id'].unique()
oclc_identifiers = list(oclc_identifiers)

# Loops through list of oclc_identifiers and searches for matches in HathiTrust.
all_results = []
for index, identifier in enumerate(oclc_identifiers):
    print(index, identifier)
    identifier = str(identifier).strip()
    search_url = hURL_brief+identifier+'.json'
    h_response = requests.get(search_url).json()
    records = h_response.get('records')
    # If matches are found, adds HathiTrust metadata to all_results.
    if records:
        for record in records:
            record_values = records.get(record)
            result = {}
            for k, v in record_values.items():
                if isinstance(v, list):
                    v = '|'.join(v)
                result[k] = v
            all_results.append(result)

# Creates DataFrame from all_results.
df_results = pd.DataFrame.from_dict(all_results)
# Creates CSV called "hathiTrustResults.csv" from DataFrame.
df_results.to_csv('hathiTrustResults.csv', index=False)