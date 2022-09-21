import time
import pandas as pd
import argparse
import requests
import googleKey
import math

# This script searches Google Books for OCLC numbers from a CSV and creates a new CSV with the metadata of any matches.

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Enter filename with csv.')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.csv\'): ')

# API Key access
key = googleKey.key
baseURL = 'https://www.googleapis.com/books/v1/volumes?q='

# Reads CSV as DataFrame, grabs OCLC identifiers from column named "oclc_id."
df = pd.read_csv(filename, dtype={'oclc_id': str})
df.dropna(subset=['oclc_id'], inplace=True)   # Drop blank values.
oclc_identifiers = df['oclc_id'].unique()
oclc_identifiers = list(oclc_identifiers)

# Math to find when the script should pause for 60 seconds.
x = len(oclc_identifiers)/100
x = math.ceil(x)
list_x = list(range(x))
if 0 in list_x:
    list_x.remove(0)
list_x = [n*100 for n in list_x]
print(list_x)

# Loops through list of oclc_identifiers and searches for matches in Google Books.
all_results = []
for index, identifier in enumerate(oclc_identifiers):
    print(index, identifier)
    identifier = identifier.strip()
    results = requests.get(baseURL+'oclc:'+identifier+'&key='+key).json()
    print(results)
    time.sleep(.5)
    if results['totalItems'] > 0:
        for item in results['items']:
            result = {'GB_oclc': identifier}
            metadata = item['volumeInfo']
            result['GB_link'] = metadata.get('canonicalVolumeLink')
            result['GB_title'] = metadata.get('title')
            authors = metadata.get('authors')
            authors = '|'.join(authors)
            result['GB_authors'] = authors
            result['GB_publisher'] = metadata.get('publisher')
            result['GB_publishDate'] = metadata.get('publishedDate')
            all_results.append(result)
    if index+1 in list_x:
        time.sleep(60)


# Creates DataFrame from all_results.
df_results = pd.DataFrame.from_dict(all_results)
# Creates CSV called "googleBooksResults.csv" from DataFrame.
df_results.to_csv('googleBooksResults.csv', index=False)