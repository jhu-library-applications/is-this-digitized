import pandas as pd
from internetarchive import get_session, search_items
import argparse

# This script searches Internet Archive for OCLC numbers from a CSV and creates a new CSV with the metadata of any
# matches.

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Enter filename with csv.')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.csv\'): ')

# Reads CSV as DataFrame, grabs OCLC identifiers from column named "oclc_id."
df = pd.read_csv(filename)
df.dropna(subset=['oclc_id'], inplace=True)  # Drop blank values.
oclc_identifiers = df['oclc_id'].unique()
oclc_identifiers = list(oclc_identifiers)

s = get_session()

fields = ['identifier', 'title', 'date', 'language', 'publisher', 'source', 'contributor', 'creator']

# Loops through list of oclc_identifiers and searches for matches in the Internet Archive.
all_results = []
for index, identifier in enumerate(oclc_identifiers):
    print(index, identifier)
    identifier = str(identifier)
    params = {'rows': 10, 'page': 1}
    search = s.search_items('external-identifier:"urn:oclc:record:'+identifier+'"', params=params, fields=fields)
    for result in search:
        result['oclc'] = identifier
        all_results.append(result)
    search_2 = s.search_items('oclc_id:"'+identifier+'"', params=params, fields=fields)
    for result in search_2:
        result['oclc'] = identifier
        all_results.append(result)

# Creates DataFrame from all_results.
df_results = pd.DataFrame.from_dict(all_results)
# Creates CSV called "internetArchiveResults.csv" from DataFrame.
df_results.to_csv('internetArchiveResults_test.csv', index=False)