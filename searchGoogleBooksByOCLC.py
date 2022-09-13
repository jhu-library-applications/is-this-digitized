import time
import pandas as pd
import argparse
import requests
import googleKey

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
df = pd.read_csv(filename)
df.dropna(subset=['oclc_id'], inplace=True)   # Drop blank values.
oclc_identifiers = df['oclc_id'].unique()
oclc_identifiers = list(oclc_identifiers)

x = len(oclc_identifiers)/100
x = round(x)
list_x = list(range(x))
if 0 in list_x:
    list_x.remove(0)
list_x = [n*100 for n in list_x]
print(list_x)

# Loops through list of oclc_identifiers and searches for matches in Google Books.
all_results = []
for index, identifier in enumerate(oclc_identifiers):
    print(index, identifier)
    identifier = str(identifier).strip()
    results = requests.get(baseURL+'oclc:'+identifier+'&key='+key).json()
    print(results)
    if results['totalItems'] > 0:
        for item in results['items']:
            result = {'oclc': identifier}
            result['link'] = item['selfLink']
            metadata = item['volumeInfo']
            result['title'] = metadata.get('title')
            result['authors'] = metadata.get('authors')
            result['publisher'] = metadata.get('publisher')
            result['date'] = metadata.get('publishedDate')
            all_results.append(result)
    if index+1 in list_x:
        time.sleep(60)


# Creates DataFrame from all_results.
df_results = pd.DataFrame.from_dict(all_results)
# Creates CSV called "googleBooksResults.csv" from DataFrame.
df_results.to_csv('googleBooksResults.csv', index=False)